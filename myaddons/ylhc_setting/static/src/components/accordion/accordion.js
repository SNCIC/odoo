/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class YlhcAccordion extends Component {

    setup() {
        super.setup();
        this.state = useState({
            'collapse': true
        })
    }

    toggleDisplay() {
        this.state.collapse = !this.state.collapse;
    }
};

YlhcAccordion.props = {
    title: {
        type: String
    },
    slots: {
        type: Object,
        optional: true,
    },
};

YlhcAccordion.template = "ylhc_setting.accordion";
YlhcAccordion.components = {};
