/** @odoo-module  **/

import { Component, useState, useRef } from "@odoo/owl";


export class MaskChecker extends Component {

    setup() {
        super.setup();
        this.root = useRef('root');
    }

    /**
     * on mask click
     * @param {*} ev 
     */
    _on_mask_click() {
        this.props.onChecked();
    }

    _on_mask_hover() {
        if (this.props.onEnter) {
            this.props.onEnter(this.root.el);
        }
    }

    _on_mask_leave(event) {
        if (this.props.onLeave) {
            this.props.onLeave(this.root.el);
        }
    }
};

MaskChecker.props = {
    onChecked: {
        type: Function,
        optional: 1,
    },
    checked: {
        type: Boolean,
        optional: 1,
    },
    slots: {
        type: Object,
        optional: true,
    },
    extraClass: {
        type: String,
        optional: true,
    },
    onEnter: {
        type: Function,
        optional: 1,
    },
    onLeave: {
        type: Function,
        optional: 1,
    },
};

MaskChecker.template = "ylhc_setting.mask_checker";

