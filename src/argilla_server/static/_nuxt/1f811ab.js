(window.webpackJsonp=window.webpackJsonp||[]).push([[16,36,49,59,141,216],{1032:function(e,t,n){"use strict";n.r(t);n(753);var i=n(281),a={directives:{clickOutside:n.n(i).a.directive},props:{modalCloseButton:{type:Boolean,default:!0},modalVisible:{type:Boolean,default:!0},allowClose:{type:Boolean,default:!1},modalClass:{type:String,default:"modal-info"},modalIcon:{type:String},modalTitle:{type:String,default:void 0},preventBodyScroll:{type:Boolean,default:!1},messages:{type:Array,default:function _default(){return[]}},modalPosition:{type:String,default:"modal-center"}},computed:{modalMaskClass:function modalMaskClass(){return this.preventBodyScroll?"prevent-scroll":null}},methods:{closeModal:function closeModal(){this.$emit("close-modal")}}},s=(n(974),n(39)),o=Object(s.a)(a,(function render(){var e=this,t=e._self._c;return e.modalVisible?t("transition",{attrs:{name:"modal",appear:""}},[t("div",{staticClass:"modal-mask",class:e.modalMaskClass},[t("div",{staticClass:"modal-wrapper",class:e.modalPosition},[t("div",{directives:[{name:"click-outside",rawName:"v-click-outside",value:e.closeModal,expression:"closeModal"}],staticClass:"modal-container",class:e.modalClass},[e.modalTitle?t("p",{staticClass:"modal__title"},[e._v("\n          "+e._s(e.modalTitle)+"\n        ")]):e._e(),e._v(" "),e._t("default"),e._v(" "),e.allowClose?t("BaseButton",{staticClass:"button-close-modal",on:{"on-click":e.closeModal}},[t("svgicon",{attrs:{name:"close",width:"20",height:"20"}})],1):e._e()],2)])])]):e._e()}),[],!1,null,"2051a077",null);t.default=o.exports;installComponents(o,{BaseButton:n(415).default})},1114:function(e,t,n){var i=n(1288);i.__esModule&&(i=i.default),"string"==typeof i&&(i=[[e.i,i,""]]),i.locals&&(e.exports=i.locals);(0,n(82).default)("798f65a7",i,!0,{sourceMap:!1})},1287:function(e,t,n){"use strict";n(1114)},1288:function(e,t,n){var i=n(81),a=n(85),s=n(86),o=n(87),r=i((function(e){return e[1]})),c=a(s),l=a(o);r.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+c+') format("woff2"),url('+l+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.card{align-items:flex-end;border:1px solid rgba(0,0,0,.1);border-radius:5px;display:flex;padding:16px}.card__buttons{margin-left:auto}.card__title{margin-top:0}.card__text{color:rgba(0,0,0,.37);margin-bottom:0}',""]),r.locals={},e.exports=r},1324:function(e,t,n){"use strict";n.r(t);n(67);var i={props:{title:{type:String},subtitle:{type:String},text:{type:String},buttonText:{type:String},cardType:{type:String,default:"default",validator:function validator(e){return["danger","warm","info","default"].includes(e)}}},computed:{cardClasses:function cardClasses(){return{"--danger":"danger"===this.cardType,"--warm":"warm"===this.cardType,"--info":"info"===this.cardType,"--default":"default"===this.cardType}}},methods:{action:function action(){this.$emit("card-action")}}},a=(n(1287),n(39)),s=Object(a.a)(i,(function render(){var e=this,t=e._self._c;return t("div",{staticClass:"card",class:[e.cardClasses]},[t("div",{staticClass:"card__content"},[e.title?t("h3",{staticClass:"--body1 --light card__title",domProps:{innerHTML:e._s(e.title)}}):e._e(),e._v(" "),e.subtitle?t("h4",{staticClass:"--body2 --semibold card__subtitle"},[e._v("\n      "+e._s(e.subtitle)+"\n    ")]):e._e(),e._v(" "),e.text?t("p",{staticClass:"--body1 card__text"},[e._v("\n      "+e._s(e.text)+"\n    ")]):e._e()]),e._v(" "),e.buttonText?t("div",{staticClass:"card__buttons"},[t("base-button",{staticClass:"card__button outline small",class:[e.cardClasses],on:{click:e.action}},[e._v(e._s(e.buttonText))])],1):e._e()])}),[],!1,null,null,null);t.default=s.exports;installComponents(s,{BaseButton:n(415).default})},1434:function(e,t,n){var i=n(1527);i.__esModule&&(i=i.default),"string"==typeof i&&(i=[[e.i,i,""]]),i.locals&&(e.exports=i.locals);(0,n(82).default)("9c6eeb78",i,!0,{sourceMap:!1})},1490:function(e,t,n){"use strict";n.r(t);var i=n(4),a=n(18),s=(n(12),n(17),n(30),n(45),n(25),n(29),n(6),n(50),n(23),n(51),n(146)),o=n(170),r=n(282);function ownKeys(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);t&&(i=i.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,i)}return n}function _objectSpread(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?ownKeys(Object(n),!0).forEach((function(t){Object(a.a)(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):ownKeys(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}var c={props:{datasetId:{type:Array,required:!0},datasetTask:{type:String,required:!0}},data:function data(){return{sectionTitle:"Danger zone",showDeleteModal:!1}},computed:{dataset:function dataset(){return Object(r.a)(this.datasetId,this.datasetTask)},datasetName:function datasetName(){var e;return null===(e=this.dataset)||void 0===e?void 0:e.name},datasetDeleteTitle:function datasetDeleteTitle(){return"Delete <strong>".concat(this.datasetName,"</strong>")},modalTitle:function modalTitle(){return"Delete confirmation"},modalDescription:function modalDescription(){return"You are about to delete: <strong>".concat(this.datasetName,"</strong> from workspace <strong>").concat(this.workspace,"</strong>. This action cannot be undone")},workspace:function workspace(){return Object(o.a)(this.$route)}},methods:_objectSpread(_objectSpread({},Object(s.b)({deleteDataset:"entities/datasets/deleteDataset"})),{},{onConfirmDeleteDataset:function onConfirmDeleteDataset(){var e=this;return Object(i.a)(regeneratorRuntime.mark((function _callee(){var t;return regeneratorRuntime.wrap((function _callee$(n){for(;;)switch(n.prev=n.next){case 0:return n.prev=0,n.next=3,e.deleteSelectedDataset();case 3:e.goToDatasetList(),n.next=10;break;case 6:n.prev=6,n.t0=n.catch(0),"NOT_ALLOWED_TO_UPDATE_LABELS"===(t=n.t0.response)?console.log("user is not allowed to delete dataset"):console.log(t);case 10:return n.prev=10,e.toggleDeleteModal(!1),n.finish(10);case 13:case"end":return n.stop()}}),_callee,null,[[0,6,10,13]])})))()},toggleDeleteModal:function toggleDeleteModal(e){this.showDeleteModal=e},goToDatasetList:function goToDatasetList(){this.$router.push("/")},deleteSelectedDataset:function deleteSelectedDataset(){var e=this;return Object(i.a)(regeneratorRuntime.mark((function _callee2(){return regeneratorRuntime.wrap((function _callee2$(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,e.deleteDataset({workspace:e.workspace,name:e.datasetName});case 2:case"end":return t.stop()}}),_callee2)})))()}})},l=(n(1526),n(39)),d=Object(l.a)(c,(function render(){var e=this,t=e._self._c;return e.datasetName?t("div",{staticClass:"dataset-delete"},[t("h2",{staticClass:"--heading5 --medium"},[e._v(e._s(e.sectionTitle))]),e._v(" "),t("base-card",{attrs:{"card-type":"danger",title:e.datasetDeleteTitle,text:"Be careful, this action is not reversible",buttonText:"Delete dataset"},on:{"card-action":function cardAction(t){return e.toggleDeleteModal(!0)}}}),e._v(" "),t("base-modal",{staticClass:"delete-modal",attrs:{"modal-custom":!0,"prevent-body-scroll":!0,"modal-class":"modal-secondary","modal-title":e.modalTitle,"modal-visible":e.showDeleteModal},on:{"close-modal":function closeModal(t){return e.toggleDeleteModal(!1)}}},[t("div",[t("p",{domProps:{innerHTML:e._s(e.modalDescription)}}),e._v(" "),t("div",{staticClass:"modal-buttons"},[t("base-button",{staticClass:"primary outline",on:{click:function click(t){return e.toggleDeleteModal(!1)}}},[e._v("\n          Cancel\n        ")]),e._v(" "),t("base-button",{staticClass:"primary",on:{click:e.onConfirmDeleteDataset}},[e._v("\n          Yes, delete\n        ")])],1)])])],1):e._e()}),[],!1,null,"74abe4ad",null);t.default=d.exports;installComponents(d,{BaseCard:n(1324).default,BaseButton:n(415).default,BaseModal:n(1032).default})},1526:function(e,t,n){"use strict";n(1434)},1527:function(e,t,n){var i=n(81),a=n(85),s=n(86),o=n(87),r=i((function(e){return e[1]})),c=a(s),l=a(o);r.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+c+') format("woff2"),url('+l+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.dataset-delete[data-v-74abe4ad]{margin-bottom:40px}',""]),r.locals={},e.exports=r},753:function(e,t,n){n(178).register({close:{width:41,height:40,viewBox:"0 0 41 40",data:'<path pid="0" d="M8.922 5.587a2.005 2.005 0 10-2.835 2.835L17.665 20 6.087 31.577a2.005 2.005 0 102.836 2.836L20.5 22.835l11.577 11.578a2.005 2.005 0 002.836-2.836L23.335 20 34.913 8.422a2.005 2.005 0 00-2.835-2.835L20.5 17.165 8.922 5.587z" _fill="#000"/>'}})},840:function(e,t,n){var i=n(975);i.__esModule&&(i=i.default),"string"==typeof i&&(i=[[e.i,i,""]]),i.locals&&(e.exports=i.locals);(0,n(82).default)("2b9e83e6",i,!0,{sourceMap:!1})},974:function(e,t,n){"use strict";n(840)},975:function(e,t,n){var i=n(81),a=n(85),s=n(86),o=n(87),r=i((function(e){return e[1]})),c=a(s),l=a(o);r.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+c+') format("woff2"),url('+l+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.modal-mask[data-v-2051a077]{background:rgba(0,0,0,.2);cursor:default;display:table;height:100vh;left:0;position:fixed;top:0;transition:opacity .3s ease;width:100%;z-index:9998}.modal-mask[data-v-2051a077]:not(.prevent-scroll){pointer-events:none}.modal-wrapper[data-v-2051a077]{display:flex;height:100vh}.modal-wrapper.modal-bottom-right[data-v-2051a077]{align-items:flex-end;padding-bottom:3.5em}.modal-wrapper.modal-bottom-right .modal-container[data-v-2051a077]{margin-right:1.5em}.modal-wrapper.modal-top-right[data-v-2051a077]{align-items:flex-start;padding-top:10em}.modal-wrapper.modal-top-right .modal-container[data-v-2051a077]{margin-right:6em}.modal-wrapper.modal-top-center[data-v-2051a077]{align-items:flex-start;padding-top:5em}.modal-wrapper.modal-center[data-v-2051a077]{align-items:center}.modal-container[data-v-2051a077]{background-color:#fff;border-radius:5px;box-shadow:0 8px 20px 0 rgba(0,0,0,.2);color:rgba(0,0,0,.87);margin:0 auto;max-width:460px;padding:32px;pointer-events:all;position:relative;text-align:left;transition:all .5s}.button-close-modal[data-v-2051a077]{padding:0;position:absolute;right:16px;top:16px}.modal-primary[data-v-2051a077]{border-radius:5px;box-shadow:0 8px 20px 0 rgba(0,0,0,.2);max-width:520px}.modal-primary[data-v-2051a077] .modal__text{margin-bottom:2em}.modal-secondary[data-v-2051a077]{border-radius:5px;box-shadow:0 8px 20px 0 rgba(0,0,0,.2);max-width:440px}.modal-secondary[data-v-2051a077] .modal__text{margin-bottom:2em}.modal-table[data-v-2051a077]{border-radius:5px;box-shadow:0 8px 20px 0 rgba(0,0,0,.2);max-width:none}.modal-table[data-v-2051a077] .modal__text{margin-bottom:2em}.modal-auto[data-v-2051a077]{border-radius:5px;box-shadow:0 8px 20px 0 rgba(0,0,0,.2);max-width:none}.modal-auto[data-v-2051a077] .modal__text{margin-bottom:2em}[data-v-2051a077] .modal-buttons{display:flex}[data-v-2051a077] .modal-buttons .button{justify-content:center;width:100%}[data-v-2051a077] .modal-buttons .button:last-child{margin-left:16px}[data-v-2051a077] .modal__title{align-items:center;display:flex;font-size:16px;font-size:1rem;font-weight:600;gap:8px;margin-top:0}.modal-enter[data-v-2051a077],.modal-leave-active[data-v-2051a077]{opacity:0}.modal-enter .modal-container[data-v-2051a077],.modal-leave-active .modal-container[data-v-2051a077]{transform:scale(.99)}',""]),r.locals={},e.exports=r}}]);