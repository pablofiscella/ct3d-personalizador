<?php
/**
 * Plugin Name: CT3D · Kit Personalizado (Un Añito Salvaje)
 * Description: Campos de personalización + vista previa en vivo en el producto, y generación automática del kit (ZIP de PDFs) al pagar, vía el servicio Python de CT3D.
 * Version: 1.0
 * Author: Casa Tridimensional
 * Requires Plugins: woocommerce
 */
if (!defined('ABSPATH')) exit;

class CT3D_Kit {
    const OPT = 'ct3d_kit_opts';
    /** campos que llena el cliente (deben coincidir con CAMPOS del servicio Python) */
    static function campos() {
        return array(
            'edad'      => 'Edad que cumple',
            'nombre'    => 'Nombre del cumpleañero/a',
            'fecha'     => 'Fecha',
            'hora'      => 'Hora',
            'lugar'     => 'Salón / lugar (opcional)',
            'direccion' => 'Dirección del lugar',
            'telefono'  => 'Teléfono para confirmar',
        );
    }
    static function opts() {
        return wp_parse_args(get_option(self::OPT, array()), array(
            'service_url' => 'http://192.168.1.251:8787',
            'api_key'     => '',
        ));
    }

    static function init() {
        // --- Admin: marcar un producto como "kit personalizable" ---
        add_action('woocommerce_product_options_general_product_data', array(__CLASS__, 'product_checkbox'));
        add_action('woocommerce_process_product_meta', array(__CLASS__, 'save_product_checkbox'));

        // --- Front: campos + preview en el producto ---
        add_action('woocommerce_before_add_to_cart_button', array(__CLASS__, 'product_fields'));
        add_filter('woocommerce_add_to_cart_validation', array(__CLASS__, 'validate'), 10, 2);
        add_filter('woocommerce_add_cart_item_data', array(__CLASS__, 'add_cart_item_data'), 10, 2);
        add_filter('woocommerce_get_item_data', array(__CLASS__, 'show_cart_item_data'), 10, 2);
        add_action('woocommerce_checkout_create_order_line_item', array(__CLASS__, 'save_order_item'), 10, 4);

        // --- Al pagar: generar el kit ---
        add_action('woocommerce_order_status_processing', array(__CLASS__, 'generate_for_order'));
        add_action('woocommerce_order_status_completed', array(__CLASS__, 'generate_for_order'));

        // --- Mostrar link de descarga al cliente ---
        add_action('woocommerce_order_details_after_order_table', array(__CLASS__, 'download_block'));
        add_action('woocommerce_email_after_order_table', array(__CLASS__, 'download_block_email'), 10, 1);

        // --- Settings ---
        add_action('admin_menu', array(__CLASS__, 'settings_menu'));
        add_action('admin_init', array(__CLASS__, 'settings_register'));
    }

    /* ---------------- Producto: checkbox ---------------- */
    static function product_checkbox() {
        woocommerce_wp_checkbox(array(
            'id' => '_ct3d_kit',
            'label' => 'Kit personalizable CT3D',
            'description' => 'Mostrar campos de personalización y generar el kit al pagar.',
        ));
        woocommerce_wp_text_input(array(
            'id' => '_ct3d_tema',
            'label' => 'Temática CT3D (id)',
            'placeholder' => 'safari',
            'description' => 'El id de la temática a generar (ver en el panel de temáticas). Por defecto: safari.',
            'desc_tip' => true,
        ));
    }
    static function save_product_checkbox($post_id) {
        update_post_meta($post_id, '_ct3d_kit', isset($_POST['_ct3d_kit']) ? 'yes' : 'no');
        $tema = isset($_POST['_ct3d_tema']) ? sanitize_text_field($_POST['_ct3d_tema']) : '';
        update_post_meta($post_id, '_ct3d_tema', $tema ? $tema : 'safari');
    }
    static function is_kit($product_id) {
        return get_post_meta($product_id, '_ct3d_kit', true) === 'yes';
    }
    static function tema_de($product_id) {
        $t = get_post_meta($product_id, '_ct3d_tema', true);
        return $t ? $t : 'safari';
    }

    /* ---------------- Producto: campos + preview ---------------- */
    static function product_fields() {
        global $product;
        if (!$product || !self::is_kit($product->get_id())) return;
        $o = self::opts();
        $preview = trailingslashit($o['service_url']) . 'preview';
        echo '<div class="ct3d-kit-form" style="margin:18px 0;display:grid;gap:20px;grid-template-columns:1fr 1fr;align-items:start">';
        echo '<div>';
        echo '<h4 style="margin:.2em 0 .6em">Personalizá tu kit 🦁</h4>';
        foreach (self::campos() as $key => $label) {
            if ($key === 'edad') {
                echo '<p style="margin:0 0 10px"><label for="ct3d_edad" style="display:block;font-size:.85em;font-weight:600">' . esc_html($label) . ' *</label>
                      <select id="ct3d_edad" name="ct3d[edad]" style="width:100%;padding:9px 11px;border:1px solid #ccc;border-radius:8px">
                        <option value="1">1 año</option><option value="2">2 años</option><option value="3">3 años</option>
                      </select></p>';
                continue;
            }
            $ph = $key === 'nombre' ? 'Tomás' : '';
            printf(
                '<p style="margin:0 0 10px"><label for="ct3d_%1$s" style="display:block;font-size:.85em;font-weight:600">%2$s%3$s</label>
                 <input type="text" id="ct3d_%1$s" name="ct3d[%1$s]" maxlength="40" placeholder="%4$s" style="width:100%%;padding:9px 11px;border:1px solid #ccc;border-radius:8px"></p>',
                esc_attr($key), esc_html($label),
                $key === 'nombre' ? ' *' : '', esc_attr($ph)
            );
        }
        echo '</div>';
        echo '<div style="text-align:center">
                <img id="ct3d-preview-img" alt="Vista previa" style="max-width:100%;border-radius:10px;box-shadow:0 6px 18px rgba(0,0,0,.12)">
                <p style="font-size:.75em;opacity:.7;margin-top:8px">Vista previa de la invitación. El kit completo (7 piezas) se genera con estos datos.</p>
              </div>';
        echo '</div>';
        // JS de preview en vivo (debounce -> /preview del servicio)
        $fields = wp_json_encode(array_keys(self::campos()));
        $svc = esc_js(rtrim($o['service_url'], '/'));
        $tema = esc_js(self::tema_de($product->get_id()));
        echo "<script>(function(){
            var svc='{$svc}', tema='{$tema}', fields={$fields}, img=document.getElementById('ct3d-preview-img'), t;
            function upd(){clearTimeout(t);t=setTimeout(function(){
                var p=new URLSearchParams();
                fields.forEach(function(f){var e=document.getElementById('ct3d_'+f); if(e)p.set(f,e.value);});
                if(!p.get('nombre'))p.set('nombre','Tomás');
                p.set('tema', tema);
                img.src=svc+'/preview?'+p.toString()+'&_t='+Date.now();
            },500);}
            fields.forEach(function(f){var e=document.getElementById('ct3d_'+f); if(e){e.addEventListener('input',upd);e.addEventListener('change',upd);}});
            upd();
        })();</script>";
    }

    static function validate($passed, $product_id) {
        if (self::is_kit($product_id)) {
            if (empty($_POST['ct3d']['nombre']) || !trim($_POST['ct3d']['nombre'])) {
                wc_add_notice('Escribí el nombre del cumpleañero/a para personalizar el kit.', 'error');
                return false;
            }
        }
        return $passed;
    }

    static function add_cart_item_data($cart_item_data, $product_id) {
        if (self::is_kit($product_id) && !empty($_POST['ct3d'])) {
            $data = array();
            foreach (array_keys(self::campos()) as $k) {
                $data[$k] = isset($_POST['ct3d'][$k]) ? sanitize_text_field(wp_unslash($_POST['ct3d'][$k])) : '';
            }
            $cart_item_data['ct3d_kit'] = $data;
            $cart_item_data['ct3d_uid'] = md5(wp_json_encode($data) . microtime()); // líneas separadas por datos
        }
        return $cart_item_data;
    }

    static function show_cart_item_data($items, $cart_item) {
        if (!empty($cart_item['ct3d_kit'])) {
            $c = self::campos();
            foreach ($cart_item['ct3d_kit'] as $k => $v) {
                if ($v !== '') $items[] = array('key' => $c[$k], 'value' => wc_clean($v));
            }
        }
        return $items;
    }

    static function save_order_item($item, $cart_item_key, $values, $order) {
        if (!empty($values['ct3d_kit'])) {
            $c = self::campos();
            foreach ($values['ct3d_kit'] as $k => $v) {
                if ($v !== '') $item->add_meta_data($c[$k], $v, true);
            }
            $item->add_meta_data('_ct3d_kit_data', $values['ct3d_kit'], true); // crudo, oculto
        }
    }

    /* ---------------- Generación al pagar ---------------- */
    static function generate_for_order($order_id) {
        $order = wc_get_order($order_id);
        if (!$order) return;
        if ($order->get_meta('_ct3d_generado') === 'yes') return; // idempotente

        $o = self::opts();
        $links = array();
        foreach ($order->get_items() as $item_id => $item) {
            $data = $item->get_meta('_ct3d_kit_data', true);
            if (empty($data) || empty($data['nombre'])) continue;

            $body = array_merge($data, array(
                'order_id' => (string) $order_id,
                'email'    => $order->get_billing_email(),
                'tema'     => self::tema_de($item->get_product_id()),
            ));
            $resp = wp_remote_post(trailingslashit($o['service_url']) . 'api/generar', array(
                'timeout' => 120,
                'headers' => array('Content-Type' => 'application/json', 'X-API-Key' => $o['api_key']),
                'body'    => wp_json_encode($body),
            ));
            if (is_wp_error($resp)) {
                $order->add_order_note('CT3D: error al generar kit — ' . $resp->get_error_message());
                continue;
            }
            $json = json_decode(wp_remote_retrieve_body($resp), true);
            if (!empty($json['ok']) && !empty($json['download_url'])) {
                $links[] = array('nombre' => $data['nombre'], 'url' => $json['download_url']);
                wc_update_order_item_meta($item_id, '_ct3d_download', $json['download_url']);
            } else {
                $order->add_order_note('CT3D: respuesta inesperada del servicio — ' . wp_remote_retrieve_body($resp));
            }
        }
        if ($links) {
            $order->update_meta_data('_ct3d_links', $links);
            $order->update_meta_data('_ct3d_generado', 'yes');
            $order->save();
            $order->add_order_note('CT3D: kit(s) generado(s) correctamente (' . count($links) . ').');
        }
    }

    /* ---------------- Mostrar descargas ---------------- */
    static function download_block($order) {
        $links = $order->get_meta('_ct3d_links');
        if (empty($links)) return;
        echo '<section class="ct3d-downloads" style="margin:20px 0;padding:16px;border:1px solid #e4d8c5;border-radius:12px;background:#fbf7ef">';
        echo '<h2 style="margin-top:0">🦁 Tu kit imprimible</h2><ul>';
        foreach ($links as $l) {
            printf('<li><a href="%s" style="font-weight:600">Descargar kit de %s (ZIP)</a></li>',
                esc_url($l['url']), esc_html($l['nombre']));
        }
        echo '</ul><p style="font-size:.8em;opacity:.75">Son PDFs listos para imprimir (300 DPI). Si todavía no aparece, esperá unos segundos tras la confirmación del pago.</p></section>';
    }
    static function download_block_email($order) {
        if (is_a($order, 'WC_Order')) self::download_block($order);
    }

    /* ---------------- Settings ---------------- */
    static function settings_menu() {
        add_submenu_page('woocommerce', 'CT3D Kit', 'CT3D Kit', 'manage_woocommerce', 'ct3d-kit', array(__CLASS__, 'settings_page'));
    }
    static function settings_register() {
        register_setting('ct3d_kit_group', self::OPT);
    }
    static function settings_page() {
        $o = self::opts(); ?>
        <div class="wrap"><h1>CT3D · Kit Personalizado</h1>
        <form method="post" action="options.php"><?php settings_fields('ct3d_kit_group'); ?>
        <table class="form-table">
          <tr><th>URL del servicio Python</th>
            <td><input type="text" name="<?php echo self::OPT; ?>[service_url]" value="<?php echo esc_attr($o['service_url']); ?>" class="regular-text" placeholder="http://192.168.1.251:8787"></td></tr>
          <tr><th>API Key (CT3D_API_KEY)</th>
            <td><input type="text" name="<?php echo self::OPT; ?>[api_key]" value="<?php echo esc_attr($o['api_key']); ?>" class="regular-text"></td></tr>
        </table>
        <?php submit_button(); ?></form>
        <p>Debe coincidir con la <code>CT3D_API_KEY</code> con la que corre <code>servicio.py</code> en CT101.</p></div>
        <?php
    }
}
add_action('plugins_loaded', array('CT3D_Kit', 'init'));
