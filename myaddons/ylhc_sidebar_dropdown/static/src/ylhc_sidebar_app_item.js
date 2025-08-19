/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { Component, useState, onMounted, onWillUnmount, markup } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { SideBarAppItem } from "@ylhc_theme/sidebar/ylhc_sidebar_app_item";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { useBus, useService } from "@web/core/utils/hooks";

patch(SideBarAppItem.prototype, {

    setup() {
        super.setup();
        this.state = useState({ 
            collapsed: false,
        });
        useBus(this.env.bus, "YLHC_SIDEBAR_COLLAPSED", ({ detail: collapsed }) => {
            this.state.collapsed = collapsed;
        });
    }
    
});

SideBarAppItem.Component = {
    ...SideBarAppItem.Component,
    Dropdown,
}

