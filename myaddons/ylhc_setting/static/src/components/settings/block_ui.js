/** @odoo-module **/

import { BlockUI } from "@web/core/ui/block_ui";
import { patch } from "@web/core/utils/patch";

import { xml } from "@odoo/owl";

import theme_setting from "ylhc_setting.theme_setting";

patch(BlockUI.prototype, {

    setup() {
        super.setup(...arguments);
        this.user_setting = theme_setting.settings;
        this.loading_style = this.user_setting.loading_svg || '/web/static/img/spin.svg';
    }

});

BlockUI.template = xml`
<div t-att-class="state.blockUI ? 'o_blockUI fixed-top d-flex justify-content-center align-items-center flex-column vh-100 bg-black-50' : ''">
  <t t-if="state.blockUI">
    <div class="o_spinner mb-4">
        <img t-att-src="this.loading_style" alt="Loading..."/>
    </div>
    <div class="o_message text-center px-4">
        <t t-esc="state.line1"/> <br/>
        <t t-esc="state.line2"/>
    </div>
  </t>
</div>`;