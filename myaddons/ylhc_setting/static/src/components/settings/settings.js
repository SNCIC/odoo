/** @odoo-module **/

import { Component, useState, onWillDestroy } from "@odoo/owl";
import { ylhcAccordion } from "../accordion/accordion";
import { MaskChecker } from "./mask_checker";

import theme_setting from "ylhc_setting.theme_setting";
let settings = theme_setting.settings || {};

export class ThemeSettings extends Component {

    setup() {
        super.setup();

        this.state = useState({
            'button_style': settings.button_style,
            'input_style': settings.input_style,
            'checkbox_style': settings.checkbox_style,
            'radio_style': settings.radio_style,
            'tab_style': settings.tab_style,
            'loading_style': settings.loading_style,
            'table_style': settings.table_style,
            'separator_style': settings.separator_style,
            'dialog_animation_in_style': settings.dialog_animation_in_style,
            'sidebar_bk_style': settings.sidebar_bk_style,
        })

        if (this.props.bus) {
            this.get_configs = this._get_configs.bind(this);
            this.props.bus.addEventListener(`get_settings`, this.get_configs);
            onWillDestroy(() => {
                this.props.bus.removeEventListener(`get_settings`, this._get_configs);
            });
        }
    }

    _get_configs(data) {
        let callback =  data.detail.callback;
        return callback && callback(this.state);
    }

    _on_style_checked(type, style) {
        switch (type) {
            case 'button':
                this.state.button_style = style;
                break;
            case 'input':
                this.state.input_style = style;
                break;
            case 'checkbox':
                this.state.checkbox_style = style;
                break;
            case 'radio':
                this.state.radio_style = style;
                break;
            case 'tab':
                this.state.tab_style = style;
                break;
            case 'loading':
                this.state.loading_style = style;
                break;
            case 'separator':
                this.state.separator_style = style;
                break;
            case 'popup':
                this.state.dialog_animation_in_style = style;
                break;
            case 'sidebar_bk':
                this.state.sidebar_bk_style = style;
                break;
        }
    }

    _on_animate(rootEl, animate, add = true) {
        if (rootEl) {
            let el = rootEl.querySelector('.animate__animated');
            if (el) {
                if (add) {
                    el.classList.add(animate);
                } else {
                    el.classList.remove(animate);
                }
            }
        }
    }
};

ThemeSettings.template = "ylhc_setting.theme_settings";
ThemeSettings.components = { MaskChecker, ylhcAccordion };