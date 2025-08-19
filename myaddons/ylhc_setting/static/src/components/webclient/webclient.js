/** @odoo-module alias=ylhc_setting.webclient**/

import { WebClient } from "@web/webclient/webclient";

import theme_setting from "ylhc_setting.theme_setting";
let settings = theme_setting.settings || {};


export class YlhcWebClient extends WebClient {
    
    setup() {
        super.setup();
        this.update_setting();

        this.env.bus.addEventListener('update_setting', (new_settings) => {
            Object.assign(theme_setting.settings, new_settings)
            settings = theme_setting.settings
            this._update_setting();
        });
    }

    /**
     * set the user setting
     */
     update_setting() {

        // update setting
        this._update_setting();

        // update the style txt 
        this._update_style();
    }

    _update_setting() {

        // show app name
        if ('show_app_name' in settings) {
            if (!settings.show_app_name) {
                document.body.classList.add('hide_app_name');
            }
        }

        // set the layout mode
        if ('layout_mode' in settings) {
            let layout_mode = settings.layout_mode
            if (layout_mode) {
                document.body.classList.add(layout_mode);
            }
        }

        // set the button style
        if ('button_style' in settings) {
            let button_style = settings.button_style
            if (button_style) {
                for (let i = 1; i <= 10; i++) {
                    document.body.classList.remove(`button_style${i}`)
                }
                document.body.classList.add('button_' + button_style)
            }    
        }

        // set the input style
        if ('input_style' in settings) {
            let input_style = settings.input_style
            if (input_style) {
                for (let i = 1; i <= 10; i++) {
                    document.body.classList.remove(`input_style${i}`)
                }
                document.body.classList.add('input_' + input_style)
            }
        }

        // tab style
        if ('tab_style' in settings) {
            let tab_style = settings.tab_style
            if (tab_style) {
                for (let i = 1; i <= 10; i++) {
                    document.body.classList.remove(`tab_${i}`)
                }
                document.body.classList.add('tab_' + tab_style)
            }
        }

        // check box style
        if ('checkbox_style' in settings) {
            let checkbox_style = settings.checkbox_style
            if (checkbox_style) {
                for (let i = 1; i <= 10; i++) {
                    document.body.classList.remove(`checkbox_style${i}`)
                }
                document.body.classList.add('checkbox_' + checkbox_style)
            }
        }

        // radio style
        if ('radio_style' in settings) {
            let radio_style = settings.radio_style
            if (radio_style) {
                for (let i = 1; i <= 10; i++) {
                    document.body.classList.remove(`radio_style${i}`)
                }
                $('body').addClass('radio_' + radio_style)
            }
        }

        // switch style
        if ('switch_style' in settings) {
            let switch_style = settings.switch_style
            if (switch_style) {
                for (let i = 1; i <= 10; i++) {
                    $('body').removeClass(`switch_style${i}`)
                }
                $('body').addClass('switch_' + switch_style)
            }
        }

        // set the rtl mode
        if ('rtl_mode' in settings) {
            if (settings.rtl_mode) {
                $('body').addClass('rtl_mode')
            }
        }

        // separator style
        if ('separator_style' in settings) {
            let separator_style = settings.separator_style
            if (separator_style) {
                for (let i = 1; i <= 10; i++) {
                    $('body').removeClass(`separator_style${i}`)
                }
                $('body').addClass('separator_' + separator_style)
            }
        }
    }

    _update_style() {

        if (theme_setting.mode_style_css) {
            let style_id = 'mode_style_id';
            let styleText = theme_setting.mode_style_css
            let style = document.getElementById(style_id);
            if (style.styleSheet) {
                style.setAttribute('type', 'text/css');
                style.styleSheet.cssText = styleText;
            } else {
                style.innerHTML = styleText;
            }
            style && document.body.removeChild(style);
            document.body.appendChild(style);
        }

        debugger
        if (theme_setting.style_css) {
            let style_id = 'style_id';
            let style_css = theme_setting.style_css;
            let style = document.getElementById(style_id);
            if (style.styleSheet) {
                style.setAttribute('type', 'text/css');
                style.styleSheet.cssText = style_css;
            } else {
                style.innerHTML = style_css;
            }
            style && document.body.removeChild(style);
            document.body.appendChild(style);
        }
    }
}
