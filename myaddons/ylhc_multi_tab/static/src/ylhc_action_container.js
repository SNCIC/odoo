/** @odoo-module **/

import { ActionContainer } from "@web/webclient/actions/action_container";
import { patch } from "@web/core/utils/patch";
import { YlhcMultiTab } from "./components/multi_tab/ylhc_multi_tab";

import {
    xml,
    useState
} from "@odoo/owl";


import { useService } from "@web/core/utils/hooks";


patch(ActionContainer.prototype, {
    
    setup() {
        super.setup(arguments);
        
        this.action_infos = useState([]);
        this.action_service = useService("action");

        // add the action to the actions stack
        this.env.bus.addEventListener("ACTION_MANAGER:UPDATE", ({ detail: info }) => {

            if (!info.Component) {
                return;
            }

            debugger
            for (let i = 0; i < this.action_infos.length; i++) {
                let action_info = this.action_infos[i];
                if (action_info == info) {
                    continue;
                }
                action_info.active = false;
            }

            // init the active state
            info.active = true;

            // get old action info
            let old_action_info = this.get_action_info(info);
            if (old_action_info) {
                let index = this.action_infos.indexOf(old_action_info);
                this.action_infos.splice(index, 1, info);
            } else {
                this.action_infos.push(info);
            }

            // remove home meunu
            let is_home_menu = false;
            if (info.action && info.action.tag == 'menu') {
                is_home_menu = true;
            }

            // remove the home menu
            if (!is_home_menu) {
                let index = this.action_infos.findIndex((action_info) => {
                    return action_info.action && action_info.action.tag == 'menu'
                })
                if (index != -1) {
                    this.action_infos.splice(index, 1);
                }
            }

            //  set current action info
            this._set_current_action_stack(info);
        });

        // close_current_tab
        this.env.bus.addEventListener("ACTION_MANAGER:CLOSE_CURRENT_TAB", () => {
            this._on_close_cur_action();
            this.env.bus.trigger("ACTION_MANAGER:UI-UPDATED");
        });
    },

    get_action_info(action_info, options) {
        if (!action_info) {
            return null;
        }
        
        let action = action_info.componentProps && action_info.componentProps.action || action_info.action;
        while (action.ref_action) {
            action = action.ref_action;
            if (action == action.ref_action) {
                break;
            }
        }

        let context = JSON.parse(JSON.stringify(action.context || {}))
        if (!context.params) {
            context.params = {}
        } else {
            delete context.params['action']
            delete context.params['cids']
            delete context.params['model']
            delete context.params['view_type']
            delete context.params['menu_id']
        }
        context.params = {}

        for(let key in context) {
            // check start with search_default_
            if (key.indexOf('search_default_') != -1) {
                delete context[key]
            }
        }

        function deepEqual(obj1, obj2) {
            if (obj1 === obj2) return true;
            
            if (typeof obj1 !== 'object' || obj1 === null ||
                typeof obj2 !== 'object' || obj2 === null) {
                return false;
            }
            
            let keys1 = Object.keys(obj1);
            let keys2 = Object.keys(obj2);
            
            if (keys1.length !== keys2.length) return false;
            
            for (let key of keys1) {
                if (!keys2.includes(key) || !deepEqual(obj1[key], obj2[key])) {
                    return false;
                }
            }
            
            return true;
        }        

        let old_action_info = this.action_infos.find((action_info) => {
            let tmp_action = action_info.componentProps.action || action_info.action;
            while (tmp_action.ref_action) {
                tmp_action = tmp_action.ref_action;
                if (tmp_action == tmp_action.ref_action) {
                    break;
                }
            }

            // clone context to prevent it
            let tmp_context = JSON.parse(JSON.stringify(tmp_action.context || {}))
            if (!tmp_context.params) {
                tmp_context.params = {}
            } else {
                delete tmp_context.params['action']
                delete tmp_context.params['cids']
                delete tmp_context.params['model']
                delete tmp_context.params['view_type']
                delete tmp_context.params['menu_id']
            }
            tmp_context.params = {}

            for(let key in tmp_context) {
                if (key.indexOf('search_default_') != -1) {
                    delete tmp_context[key]
                }
            }

            if (tmp_action.id == action.id
                && tmp_action.name == action.name
                && tmp_action.res_model == tmp_action.res_model
                && tmp_action.xml_id == action.xml_id
                && tmp_action.view_mode == action.view_mode
                && tmp_action.binding_model_id == action.binding_model_id
                && tmp_action.binding_type == action.binding_type
                && tmp_action.binding_view_types == action.binding_view_types
                && tmp_action.res_id == action.res_id
                && JSON.stringify(tmp_action.domain || {}) == JSON.stringify(action.domain || {})
                && deepEqual(tmp_context, context)) {
                return true
            } else {
                return false
            }
        })
        
        return old_action_info
    },

    _get_action(action_info) {
        let action = action_info.componentProps.action || action_info.action;
        while (action.ref_action) {
            action = action.ref_action;
            if (action == action.ref_action) {
                break;
            }
        }
        return action;
    },

    _get_action_jsId(action_info) {
        let action = this._get_action(action_info);
        return action.jsId;
    },

    _set_current_action_stack(action_info) {
        // get jsId
        let jsId = this._get_action_jsId(action_info);
        // call service function to set current action stack
        this.action_service.setCurrentAction(jsId);
        this.env.bus.trigger("MULTI_TAB:UPDATE", { jsId });
    },

    _on_active_action(action_info) {
        this._set_current_action_stack(action_info);
        // deactive all
        for (let i = 0; i < this.action_infos.length; i++) {
            let tmp_action_info = this.action_infos[i];
            tmp_action_info.active = false;
        }
        action_info.active = true;
    },

    removeActionStacks(action_info) {
        // remove the action from service
        let actionJsIds = []
        if (action_info.ref_action) {
            let ref_action = action_info.ref_action;
            while (ref_action.ref_action) {
                ref_action = ref_action.ref_action;
                if (ref_action == ref_action.ref_action) {
                    break;
                }
            }
            actionJsIds.push(ref_action.jsId)
        } else {
            if (action_info.componentProps.action) {
                actionJsIds.push(action_info.componentProps.action.jsId)
            } else if (action_info.action) {
                actionJsIds.push(action_info.action.jsId)
            }
        }
        this.action_service.removeStacks(actionJsIds)
    },

    _on_close_action(action_info) {

        action_info = this.get_action_info(action_info);
        let index = this.action_infos.indexOf(action_info);
        this.action_infos.splice(index, 1);
        
        // remove the action stack
        this.removeActionStacks(action_info);
        
        index = index - 1;
        if (index < 0) {
            index = 0;
        }
        
        // if there has no active item, maybe it not click the current item
        let bFind = false;
        for (let i = 0; i < this.action_infos.length; i++) {
            let tmp_action_info = this.action_infos[i];
            if (tmp_action_info.active) {
                bFind = true;
                break;
            }
        }
        if (!bFind && this.action_infos.length > 0) {
            this.action_infos[index].active = true;
            this._on_active_action(this.action_infos[index]);
        }
        // prevent widget reload
        this.action_service.setChangingTab(true);
    },

    _close_other_action(action_info) {
        action_info = this.get_action_info(action_info);
        let action_infos = [];
        for (let i = 0; i < this.action_infos.length; i++) {
            let tmp_action_info = this.action_infos[i];
            if(tmp_action_info != action_info) {
                action_infos.push(tmp_action_info);
            }
        }
        for (let i = 0; i < action_infos.length; i++) {
            let tmp_action_info = action_infos[i];
            let index = this.action_infos.indexOf(tmp_action_info);
            this.action_infos.splice(index, 1);
            this.removeActionStacks(tmp_action_info);
        }
    },

    _on_close_cur_action() {
        for (let i = 0; i < this.action_infos.length; i++) {
            let tmp_action_info = this.action_infos[i];
            if (tmp_action_info.active) {
                this._on_close_action(tmp_action_info)
            }
        }
    },

    _on_close_all_action() {
        this.action_infos.splice(0, this.action_infos.length);
        this.action_service.removeAllStacks();
    }
});

ActionContainer.components = {
    ...ActionContainer.components,
    YlhcMultiTab: YlhcMultiTab
};

ActionContainer.template = xml`
    <t t-name="web.ActionContainer">
        <t t-set="action_infos" t-value="action_infos" />
        <t t-debug="action_infos" />
        <div class="o_action_manager d-flex flex-colum">
            <YlhcMultiTab 
                action_infos="action_infos"
                active_action="(action_info) => this._on_active_action(action_info)"
                close_action="(action_info) => this._on_close_action(action_info)"
                close_other_action="(action_info) => this._close_other_action(action_info)"
                close_all_action="() => this._on_close_all_action()"
            />
            <div t-foreach="action_infos || []" t-as="action_info" t-if="action_info" t-key="action_info.id" class="ylhc_controller_container d-flex flex-column" t-att-class="action_info.active ? '' : 'd-none'">
                <t t-if="action_info.Component" t-component="action_info.Component" className="'o_action'" t-props="action_info.componentProps" />
            </div>
        </div>
    </t>`;
