(window.webpackJsonp=window.webpackJsonp||[]).push([[83,86],{1303:function(e,n,o){var c=o(1399);c.__esModule&&(c=c.default),"string"==typeof c&&(c=[[e.i,c,""]]),c.locals&&(e.exports=c.locals);(0,o(82).default)("95defe88",c,!0,{sourceMap:!1})},1398:function(e,n,o){"use strict";o(1303)},1399:function(e,n,o){var c=o(81),i=o(85),t=o(86),a=o(87),r=c((function(e){return e[1]})),d=i(t),s=i(a);r.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+d+') format("woff2"),url('+s+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.container[data-v-67b8bc95]{margin:0 auto;padding:4em;padding-right:126px;transition:padding .25s linear .2s}@media(min-width:1101px){.--metrics .container[data-v-67b8bc95]{padding-right:375px;transition:padding .25s linear}}.entities__container[data-v-67b8bc95]{-ms-overflow-style:none;scrollbar-width:none}.entities__container[data-v-67b8bc95]::-webkit-scrollbar{display:none}.container[data-v-67b8bc95]{margin-left:0;padding-bottom:0;padding-top:0}.entities__wrapper[data-v-67b8bc95]{position:relative}.entities__container[data-v-67b8bc95]{border-radius:10px;margin-bottom:8px;max-height:189px;overflow:auto}.--annotation .entities__container[data-v-67b8bc95]{margin-bottom:16px}.entities__container__button[data-v-67b8bc95]{display:inline-block}.entity-label[data-v-67b8bc95]{margin:4px}',""]),r.locals={},e.exports=r},1501:function(e,n,o){"use strict";o.r(n);o(48);var c={props:{labels:{type:Array,required:!0}},data:function data(){return{showExpandedList:!1,MAX_LABELS_NUMBER:10}},computed:{visibleLabels:function visibleLabels(){var visibleLabels=this.showExpandedList?this.labels:this.showMaxLabels(this.labels);return visibleLabels},numberOfLabels:function numberOfLabels(){return this.labels.length},isCollapsable:function isCollapsable(){return this.numberOfLabels>this.MAX_LABELS_NUMBER},buttonText:function buttonText(){return this.showExpandedList?"Show less":"+ ".concat(this.numberOfLabels-this.MAX_LABELS_NUMBER)}},methods:{toggleLabelsArea:function toggleLabelsArea(){this.showExpandedList=!this.showExpandedList},showMaxLabels:function showMaxLabels(e){return e.slice(0,this.MAX_LABELS_NUMBER)}}},i=(o(1398),o(39)),t=Object(i.a)(c,(function render(){var e=this,n=e._self._c;return n("div",{staticClass:"container"},[n("div",{staticClass:"entities__wrapper"},[e.numberOfLabels?n("div",{staticClass:"entities__container"},[e._l(e.visibleLabels,(function(o,c){return n("entity-label",{key:c,attrs:{label:o.text,shortcut:o.shortcut,color:"color_".concat(o.color_id%e.$entitiesMaxColors)}})})),e._v(" "),e.isCollapsable?n("base-button",{staticClass:"entities__container__button secondary text",on:{click:e.toggleLabelsArea}},[e._v("\n        "+e._s(e.buttonText)+"\n      ")]):e._e()],2):e._e()])])}),[],!1,null,"67b8bc95",null);n.default=t.exports;installComponents(t,{EntityLabel:o(923).default,BaseButton:o(415).default})},796:function(e,n,o){var c=o(880);c.__esModule&&(c=c.default),"string"==typeof c&&(c=[[e.i,c,""]]),c.locals&&(e.exports=c.locals);(0,o(82).default)("5a522cd8",c,!0,{sourceMap:!1})},879:function(e,n,o){"use strict";o(796)},880:function(e,n,o){var c=o(81),i=o(85),t=o(86),a=o(87),r=c((function(e){return e[1]})),d=i(t),s=i(a);r.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+d+') format("woff2"),url('+s+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.entity-label[data-v-050cca34]{align-items:center;color:rgba(0,0,0,.87);display:inline-flex;font-size:13px;font-size:.8125rem;font-weight:500;max-height:28px;padding:.3em;position:relative}.entity-label .shortcut[data-v-050cca34]{color:rgba(0,0,0,.6);font-weight:lighter;margin-left:16px}.color_0[data-v-050cca34]{background:#fffcc2}.color_0.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #fffcc2;padding:.3em 0}.color_1[data-v-050cca34]{background:#c8ffc2}.color_1.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c8ffc2;padding:.3em 0}.color_2[data-v-050cca34]{background:#c2fff6}.color_2.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2fff6;padding:.3em 0}.color_3[data-v-050cca34]{background:#c2cdff}.color_3.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2cdff;padding:.3em 0}.color_4[data-v-050cca34]{background:#f1c2ff}.color_4.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #f1c2ff;padding:.3em 0}.color_5[data-v-050cca34]{background:#ffc2d3}.color_5.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffc2d3;padding:.3em 0}.color_6[data-v-050cca34]{background:#ffebc2}.color_6.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffebc2;padding:.3em 0}.color_7[data-v-050cca34]{background:#d9ffc2}.color_7.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #d9ffc2;padding:.3em 0}.color_8[data-v-050cca34]{background:#c2ffe5}.color_8.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2ffe5;padding:.3em 0}.color_9[data-v-050cca34]{background:#c2deff}.color_9.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2deff;padding:.3em 0}.color_10[data-v-050cca34]{background:#e0c2ff}.color_10.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #e0c2ff;padding:.3em 0}.color_11[data-v-050cca34]{background:#ffc2e4}.color_11.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffc2e4;padding:.3em 0}.color_12[data-v-050cca34]{background:#ffdac2}.color_12.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffdac2;padding:.3em 0}.color_13[data-v-050cca34]{background:#eaffc2}.color_13.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #eaffc2;padding:.3em 0}.color_14[data-v-050cca34]{background:#c2ffd4}.color_14.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2ffd4;padding:.3em 0}.color_15[data-v-050cca34]{background:#c2efff}.color_15.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2efff;padding:.3em 0}.color_16[data-v-050cca34]{background:#cec2ff}.color_16.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #cec2ff;padding:.3em 0}.color_17[data-v-050cca34]{background:#ffc2f5}.color_17.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffc2f5;padding:.3em 0}.color_18[data-v-050cca34]{background:#ffc9c2}.color_18.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffc9c2;padding:.3em 0}.color_19[data-v-050cca34]{background:#fbffc2}.color_19.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #fbffc2;padding:.3em 0}.color_20[data-v-050cca34]{background:#c2ffc3}.color_20.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2ffc3;padding:.3em 0}.color_21[data-v-050cca34]{background:#c2fffd}.color_21.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2fffd;padding:.3em 0}.color_22[data-v-050cca34]{background:#c2c6ff}.color_22.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2c6ff;padding:.3em 0}.color_23[data-v-050cca34]{background:#f8c2ff}.color_23.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #f8c2ff;padding:.3em 0}.color_24[data-v-050cca34]{background:#ffc2cc}.color_24.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffc2cc;padding:.3em 0}.color_25[data-v-050cca34]{background:#fff2c2}.color_25.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #fff2c2;padding:.3em 0}.color_26[data-v-050cca34]{background:#d2ffc2}.color_26.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #d2ffc2;padding:.3em 0}.color_27[data-v-050cca34]{background:#c2ffec}.color_27.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2ffec;padding:.3em 0}.color_28[data-v-050cca34]{background:#c2d7ff}.color_28.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2d7ff;padding:.3em 0}.color_29[data-v-050cca34]{background:#e7c2ff}.color_29.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #e7c2ff;padding:.3em 0}.color_30[data-v-050cca34]{background:#ffc2dd}.color_30.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffc2dd;padding:.3em 0}.color_31[data-v-050cca34]{background:#ffe1c2}.color_31.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffe1c2;padding:.3em 0}.color_32[data-v-050cca34]{background:#e3ffc2}.color_32.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #e3ffc2;padding:.3em 0}.color_33[data-v-050cca34]{background:#c2ffdb}.color_33.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2ffdb;padding:.3em 0}.color_34[data-v-050cca34]{background:#c2e9ff}.color_34.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2e9ff;padding:.3em 0}.color_35[data-v-050cca34]{background:#d5c2ff}.color_35.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #d5c2ff;padding:.3em 0}.color_36[data-v-050cca34]{background:#ffc2ee}.color_36.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffc2ee;padding:.3em 0}.color_37[data-v-050cca34]{background:#ffd0c2}.color_37.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffd0c2;padding:.3em 0}.color_38[data-v-050cca34]{background:#f4ffc2}.color_38.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #f4ffc2;padding:.3em 0}.color_39[data-v-050cca34]{background:#c2ffca}.color_39.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2ffca;padding:.3em 0}.color_40[data-v-050cca34]{background:#c2faff}.color_40.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2faff;padding:.3em 0}.color_41[data-v-050cca34]{background:#c4c2ff}.color_41.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c4c2ff;padding:.3em 0}.color_42[data-v-050cca34]{background:#ffc2ff}.color_42.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffc2ff;padding:.3em 0}.color_43[data-v-050cca34]{background:#ffc2c5}.color_43.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffc2c5;padding:.3em 0}.color_44[data-v-050cca34]{background:#fff9c2}.color_44.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #fff9c2;padding:.3em 0}.color_45[data-v-050cca34]{background:#cbffc2}.color_45.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #cbffc2;padding:.3em 0}.color_46[data-v-050cca34]{background:#c2fff3}.color_46.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2fff3;padding:.3em 0}.color_47[data-v-050cca34]{background:#c2d0ff}.color_47.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #c2d0ff;padding:.3em 0}.color_48[data-v-050cca34]{background:#edc2ff}.color_48.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #edc2ff;padding:.3em 0}.color_49[data-v-050cca34]{background:#ffc2d6}.color_49.--prediction[data-v-050cca34]{background:none;border-bottom:5px solid #ffc2d6;padding:.3em 0}',""]),r.locals={},e.exports=r},923:function(e,n,o){"use strict";o.r(n);var c={props:{color:{type:String,required:!0},label:{type:String,required:!0},shortcut:{type:String,default:void 0},isPrediction:{type:Boolean,default:!1}}},i=(o(879),o(39)),t=Object(i.a)(c,(function render(){var e=this,n=e._self._c;return n("span",{class:["entity-label",e.color,e.isPrediction?"--prediction":null]},[e._v(e._s(e.label)+"\n  "),e.shortcut?n("span",{staticClass:"shortcut"},[e._v("["+e._s(e.shortcut)+"]")]):e._e()])}),[],!1,null,"050cca34",null);n.default=t.exports}}]);