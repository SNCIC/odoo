/** @odoo-module alias=ylhc_setting.theme_setting **/

let settings = {
    ...odoo.__theme_setting__
};

delete odoo.__theme_setting__;

export default settings