/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Dialog } from "@web/core/dialog/dialog"

import theme_setting from "ylhc_setting.theme_setting";
const settings = theme_setting.settings

// patch dialog
// patch(Dialog.prototype, {
//     setup() {
//         super.setup(...arguments);

//         this.dialog_animation_in_style = settings.dialog_animation_in_style;
//         if (this.dialog_animation_in_style) {
//             this.dialog_animation_in_style = 'animate__animated' + ' ' + this.dialog_animation_in_style;
//             this.props.contentClass = this.props.contentClass + ' ' + this.dialog_animation_in_style;
//         }
        
//         // wrap close
//         let _close = this.data.close;
//         this.data.close = async () => {
//             if (this.modalRef && this.modalRef.el) {
//                 let dialog_animation_out_style = settings.dialog_animation_out_style;
//                 if (dialog_animation_out_style) {
//                     // find modal-content
//                     const modalContent = this.modalRef.el.querySelector(".modal-content");
//                     if (modalContent) {
//                         // add out animation
//                         modalContent.classList.add('animate__animated', dialog_animation_out_style);
//                         // wait for animation end
//                         await new Promise((resolve) => {
//                             modalContent.addEventListener("animationend", resolve);
//                         });
//                     }
//                 }
//             }
//             // call original close
//             _close.call(this);
//         }
//     }
// });