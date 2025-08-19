/** @odoo-module **/

import { Component, useState, useExternalListener, useEffect, EventBus, useRef } from "@odoo/owl";

import { useService } from "@web/core/utils/hooks";
import { icons } from '@ylhc_setting/ylhc_icon';
import { registry } from "@web/core/registry";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { ThemeSettings } from "../settings/settings";
import { YlhcAccordion } from "@ylhc_setting/components/accordion/accordion";
import { _t } from "@web/core/l10n/translation";

import ColorPicker from "@ylhc_setting/components/color_picker/color_picker";
import theme_setting from "ylhc_setting.theme_setting";


export class ThemeCustomizer extends Component {

    setup() {
        super.setup();

        this.rpc = useService("rpc");
        this.orm = useService("orm");
        this.action = useService("action");

        this.user_setting = theme_setting;

        let cur_mode_id = this.user_setting.cur_mode_id;
        let cur_style_id = this.user_setting.cur_style_id;

        this._t = _t;

        this.icons = icons;
        this.rootRef = useRef('root');

        this.owner = false
        this.setting_component_bus = new EventBus();

        useExternalListener(window, 'mousedown', (event) => {

                if (!this.state.show_panel) {
                    return;
                }

                // check left button is donw
                if (event.target.closest('.customizer') == null
                    && event.target.closest('.sp-container') == null) {
                    this.state.show_panel = false;
                }
            });

        this.state = useState({
            show_panel: false,
            cur_mode_id: cur_mode_id,
            cur_style_id: cur_style_id,
            acitve_item: 'style'
        });

        let show_delete_style = true;
        let theme_style = this._get_theme_style(cur_style_id);
        if (theme_style && theme_style.is_default) {
            show_delete_style = false;
            this.state.show_delete_style = show_delete_style;
        }

        useEffect(() => {
            if (!this.state.show_panel) {
                $('body').removeClass('setting_preview')
            } else {
                $('body').addClass('setting_preview')
            }
        }, () => [this.state.show_panel]);
    }

    _on_window_click(event) {

    }

    _on_close_click(event) {
        this.state.show_panel = false;
    }

    _on_click_style_nav_item(theme_style) {
        this.state.cur_style_id = theme_style.id;
        if (theme_style.is_default) {
            this.state.show_delete_style = false;
        }
    }

    /**
     * change the theme modes
     * @param {*} theme_mode 
     */
    _on_change_mode(theme_mode) {
        this.state.cur_mode_id = theme_mode.id;
        let theme_styles = theme_mode.theme_styles || [];
        if (theme_styles.length > 0) {
            this.state.cur_style_id = theme_styles[0].id;
        } else {
            this.state.cur_style_id = false;
        }
    }

    _update_style_tool_bar(t) {
        let style_data = this._get_theme_style(style_id);
        if (style_data.is_default) {
            this.rootRef.el.querySelector('.operation-toolbar .delete_style').style.display = 'none';
        } else {
            this.rootRef.el.querySelerctor('.operation-toolbar .delete_style').style.display = 'block';
        }
        this.rootRef.el.querySelector('.operation-toolbar').classList.remove('d-none');
    }

    async _on_toggle_click(event) {

        event.preventDefault();
        event.stopPropagation();

        this.state.show_panel = !this.state.show_panel;
    }

    _on_customizer_close_click(event) {
        event.preventDefault();
        event.stopPropagation();

        this.state.show_panel = false;
    }

    _on_preview_click(event) {

        event.preventDefault();
        event.stopPropagation();

        // set true to preview
        this._update_style(true);

        document.body.classList.add('preview')
    }

    _on_reset_click(event) {

        event.preventDefault();
        event.stopPropagation();

        // remove the preview 
        let style = document.getElementById('preview_style_id');;
        if (style.styleSheet) {
            style.setAttribute('type', 'text/css');
            style.styleSheet.cssText = '';
        } else {
            style.innerHTML = '';
        }

        style && document.body.removeChild(style);
        document.body.appendChild(style);
        document.body.classList.remove('preview')
    }

    /**
     * delete theme style
     * @param {*} theme_mode 
     * @param {*} theme_style 
     */
    async _delete_style() {

        let style_id = this._get_cur_style_id();
        await this.orm.call(
            "ylhc_setting.theme_style", "delete_style", [style_id]);

        let theme_mode = this._get_theme_mode(this._get_cur_mode_id());
        let theme_styles = theme_mode.theme_styles;
        let index = -1;
        for (let i = 0; i < theme_styles.length; i++) {
            let tmp_style = theme_styles[i];
            if (tmp_style.id == style_id) {
                index = i;
                break;
            }
        }
        theme_styles.splice(index, 1);
        if (theme_styles.length > 0) {
            this.state.cur_style_id = theme_styles[0].id;
        } else {
            this.state.cur_style_id = false;
        }
    }

    async _update_preview_mode_css() {

    }

    _get_cur_style_id() {
        return this.state.cur_style_id;
    }

    _get_cur_mode_id() {
        return this.state.cur_mode_id;
    }

    _clear_preview_data() {
        // clear the mode style data
        let style = document.getElementById('preview_mode_id');
        if (style.styleSheet) {
            style.setAttribute('type', 'text/css');
            style.styleSheet.cssText = '';
        }
        // clear the style data
        style = document.getElementById('preview_style_id');
        if (style.styleSheet) {
            style.setAttribute('type', 'text/css');
            style.styleSheet.cssText = '';
        }
    }

    _get_style_txt(theme_style, preview) {
        let style_config = theme_style.style_config;
        let variables = style_config.variables;

        let style_txt = null;
        if (!preview) {
            style_txt = ':root {';
        } else {
            style_txt = ".preview {"
        }

        for (let index = 0; index < variables.length; index++) {
            let style_var = variables[index];
            if (!style_var['name'].startsWith('--')) {
                style_txt += "\n" + `--${style_var.name}: ${style_var.value};`
            } else {
                style_txt += "\n" + `${style_var.name}: ${style_var.value};`
            }
        }

        style_txt += "};\n"
        style_txt += '\n' + theme_style.mode_css;
        style_txt += '\n' + theme_style.style_css;

        return style_txt;
    }

    async _update_style(preview) {

        let style_id = this._get_cur_style_id();
        if (!style_id) {
            return;
        }

        // get the current style infos
        let theme_style = this._get_theme_style();
        let style_txt = this._get_style_txt(theme_style, preview);

        let style = undefined;
        if (preview) {
            style = document.getElementById('preview_style_id');
        } else {
            style = document.getElementById('style_id');
        }
        if (style.styleSheet) {
            style.setAttribute('type', 'text/css');
            style.styleSheet.cssText = style_txt;
        } else {
            style.innerHTML = style_txt;
        }
        let body = document.querySelector('body');
        style && body.appendChild(style);

        if (preview) {
            body.classList.add('preview')
        } else {
            body.classList.remove('preview')
        }
    }

    async _save_style_data(style_id) {
        let style_data = this._get_theme_style(style_id);
        return await this.orm.call(
            'ylhc_setting.setting_manager', 'save_style_data', [style_id, style_data])
    }

    get_category_vars(variables, category) {
        let result = [];
        for (let index = 0; index < variables.length; index++) {
            let style_var = variables[index];
            if (style_var.category == category) {
                result.push(style_var);
            }
        }
        return result;
    }

    /**
     * add a new style
     * @param {*} event 
     */
    async _on_add_new_style(event) {
        event.stopPropagation();
        event.preventDefault();

        this._clone_style();
    }

    _get_mode_style(mode_id, style_id) {

        let mode = this.user_setting.theme_modes.find(tmp_mode => tmp_mode.id == mode_id)
        let theme_styles = mode.theme_styles
        if (!theme_styles || theme_styles.length <= 0) {
            return null;
        }

        if (!style_id) {
            return theme_styles[0]
        }

        let theme_style = theme_styles.find(tmp_style => tmp_style.id == style_id)
        return theme_style;
    }

    _on_cancel_btn_click(event) {

        event.preventDefault();
        event.stopPropagation();

        this.state.show_panel = false;
    }

    /**
     * save settings
     * @param {*} event 
     */
    async _on_save_click(event) {
        event.preventDefault();

        let style_id = this._get_cur_style_id();
        if (!style_id) {
            return;
        }

        // save the style data
        await this._save_style_data(style_id);

        // remove all the preview mode
        let body = document.querySelector('body');
        body.classList.remove('preview')

        // remove all the mode
        // let mode_id = this._get_cur_mode_id();
        // let mode = this.user_setting.theme_modes.find(mode_data => mode_data.id == mode_id)
        // for (let index = 0; index < this.user_setting.theme_modes.length; index++) {
        //     let tmp_mode = this.user_setting.theme_modes[index];
        //     body.classList.remove(tmp_mode.name)
        //     body.classList.remove(tmp_mode.name + '_bk')
        // }
        // $('body').addClass(mode.name)

        // update the style
        this._update_style();

        // hide the panel
        this.state.show_panel = false;
    }

    _get_mode_data(mode_id) {
        return this.user_setting.theme_modes.find(mode => mode.id == mode_id)
    }

    /**
     * export style
     */
    async _export_style(event) {

        event.preventDefault();
        event.stopPropagation();

        let styleId = parseInt(this._get_cur_style_id());

        if (!styleId) {
            return
        }

        this.getSession().get_file({
            complete: framework.unblockUI,
            error: (error) => this.call('crash_manager', 'rpc_error', error),
            url: '/ylhc_setting/export_theme_style/' + styleId,
        });
    }

    get cur_theme_mode() {
        return this._get_theme_mode(this._get_cur_mode_id());
    }

    get cur_theme_style() {
        return this._get_theme_style(this._get_cur_style_id());
    }

    /**
     * clone and create a new style from the current style
     */
    async _clone_style() {
        let style_id = this._get_cur_style_id();
        let theme_mode = this._get_theme_mode(this._get_cur_mode_id());
        let new_style = await this.orm.call(
            'ylhc_setting.theme_style', 'clone_style', [style_id])
        theme_mode.theme_styles.push(new_style);
        this.render();
    }

    /**
     * replace style item
     */
    _update_theme_style(theme_style) {
        let modes = this.user_setting.theme_modes
        let mode_count = this.user_setting.theme_modes.length;
        for (let index = 0; index < mode_count; index++) {
            let mode = modes[index];
            let theme_styles = mode.theme_styles
            let style_index = -1;
            for (let styleIndex = 0; styleIndex < theme_styles.length; styleIndex++) {
                let tmp_style = theme_styles[styleIndex];
                if (tmp_style.id == theme_style.id) {
                    style_index = styleIndex;
                    break;
                }
            }
            if (style_index != -1) {
                theme_styles.splice(style_index, 1, theme_style);
                this.render();
                break;
            }
        }
    }

    _get_theme_style(style_id) {
        if (!style_id) {
            style_id = this.state.cur_style_id;
        }
        let modes = this.user_setting.theme_modes || [];
        if (!style_id && modes.length > 0) {
            let mode_data = modes[0];
            let theme_styles = mode_data.theme_styles || [];
            if (theme_styles.length > 0) {
                return theme_styles[0];
            }
        }
        for (let i = 0; i < modes.length; i++) {
            let mode_data = modes[i];
            let index = mode_data.theme_styles.findIndex(style => style.id == style_id);
            if (index != -1) {
                return mode_data.theme_styles[index];
            }
        }
        return null;
    }

    _get_theme_mode(mode_id) {
        let modes = this.user_setting.theme_modes;
        return modes.find(mode => mode.id == mode_id);
    }

    async _on_change_color(theme_style, theme_var, color) {
        theme_var.value = color;
        theme_var.dirty = true;
        theme_var.dirty = true;
        if (theme_var.identity) {
            theme_style.style_config.identities[theme_var.identity] = color;
            this.render();
        }
    }

    /**
     * reset preview mode
     */
    _on_reset_mode_preview() {
        document.querySelector('body').classList.remove('preview')
    }

    /**
     * preview the mode
     * @param {*} record 
     */
    async _on_wizard_preview(record) {
        let res_id = record.res_id
        let style_txt = this.orm.call('ylhc_setting.theme_mode', 'preview_mode', [res_id])
        $body.addClass("preview")
        let style = document.getElementById('theme_preview_mode_id');
        if (style.styleSheet) {
            style.setAttribute('type', 'text/css');
            style.styleSheet.cssText = style_txt;
        } else {
            style.innerHTML = style_txt;
        }
        style && document.querySelector('body').classList.remove('preview')
        document.querySelector('body').appendChild(style);
    }

    async _reset_variables(style_item_id) {
        let result = await this.orm.call('ylhc_setting.style_item', 'reset_var', [style_item_id])
        if (result) {
            this._reload_style_item(style_item_id)
        }
    }

    /**
     * set prveiw bk image
     */
    _set_preview_bk_image(image_url) {
        let style_id = this.state.cur_style_id;
        let theme_style = this._get_theme_style(style_id);
        theme_style.background_image = image_url;
    }

    /**
     * set theme background image
     */
    _set_bk_image() {

        let style_id = this._get_cur_style_id();
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'ylhc_setting.image_wizard',
            view_type: 'form',
            view_mode: 'form',
            target: 'new',
            views: [[false, 'form']],
            context: {
                'default_theme_style_id': style_id
            }
        }, {
            onClose: async (res) => {

                if (!res || !res.special) {
                    return
                }

                let url = await this.orm.call(
                    'ylhc_setting.theme_style', 'set_bk_image', [style_id, res.resId])
                if (url) {
                    let new_style = await this.orm.call(
                        'ylhc_setting.theme_style', 'get_style', [style_id])
                    new_style.background_image = url;
                    this._update_theme_style(new_style)
                }
            }
        })
    }

    /**
     * save the setting
     */
    _on_save_setting_click() {
        this.setting_component_bus.trigger('get_settings', {
            callback: async (settings) => {
                let new_settings = await this.orm.call(
                    'ylhc_setting.setting_manager', 'save_settings', [settings])
                this.state.show_panel = false;
                this.env.bus.trigger('update_setting', new_settings);
            }
        });
    }

    /**
     * cancel the setting
     */
    _on_cancel_setting_click() {
        this.state.show_panel = false;
    }
};

ThemeCustomizer.template = "ylhc_setting.customizer";
ThemeCustomizer.components = {
    ColorPicker: ColorPicker,
    Dropdown: Dropdown,
    DropdownItem: DropdownItem,
    ThemeSettings: ThemeSettings,
    YlhcAccordion: YlhcAccordion
};
ThemeCustomizer.props = {};

export const systrayItem = {
    Component: ThemeCustomizer
};

registry.category("systray").add(
    "ylhc_setting.customizer", systrayItem, { sequence: 1 });
