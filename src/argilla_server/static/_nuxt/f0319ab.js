(window.webpackJsonp=window.webpackJsonp||[]).push([[72],{1286:function(e,n,t){var i=t(1376);i.__esModule&&(i=i.default),"string"==typeof i&&(i=[[e.i,i,""]]),i.locals&&(e.exports=i.locals);(0,t(82).default)("4acc30c3",i,!0,{sourceMap:!1})},1375:function(e,n,t){"use strict";t(1286)},1376:function(e,n,t){var i=t(81),a=t(85),s=t(86),o=t(87),r=i((function(e){return e[1]})),c=a(s),l=a(o);r.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+c+') format("woff2"),url('+l+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.new-label[data-v-f0778682]{background:#fff;border-radius:5px;box-shadow:0 8px 20px 0 rgba(0,0,0,.2);padding:16px;position:absolute;text-align:left;top:-1em;width:180px}.new-label__close[data-v-f0778682]{stroke:rgba(0,0,0,.6);stroke-width:1;cursor:pointer;height:12px;position:absolute;right:1em;top:1.2em;width:12px}.new-label__input[data-v-f0778682]{border:0;outline:none;padding-right:2em;width:100%}.new-label__button[data-v-f0778682]{margin-top:2em}.new-label__button[data-v-f0778682],.new-label__main-button[data-v-f0778682]{margin-bottom:0!important}.new-label__main-button[data-v-f0778682]{margin-left:auto;margin-right:0}.new-label__container[data-v-f0778682]{position:relative;text-align:right}',""]),r.locals={},e.exports=r},1489:function(e,n,t){"use strict";t.r(n);t(107);var i={props:{text:{type:String,required:!1,default:"Create label"}},data:function data(){return{label:void 0,showLabelCreation:!1}},methods:{createNewLabel:function createNewLabel(e){e&&e.trim()&&(this.$emit("new-label",e),this.reset())},openLabelCreation:function openLabelCreation(){var e=this;this.showLabelCreation=!0,this.$nextTick((function(){e.$refs.labelCreation.focus()}))},reset:function reset(){this.label=void 0,this.showLabelCreation=!1}}},a=(t(1375),t(39)),s=Object(a.a)(i,(function render(){var e=this,n=e._self._c;return n("div",{staticClass:"new-label__container"},[e.showLabelCreation?n("div",{staticClass:"new-label"},[n("input",{directives:[{name:"model",rawName:"v-model",value:e.label,expression:"label"}],ref:"labelCreation",staticClass:"new-label__input",attrs:{autofocus:"",type:"text",placeholder:"New label"},domProps:{value:e.label},on:{keyup:function keyup(n){return!n.type.indexOf("key")&&e._k(n.keyCode,"enter",13,n.key,"Enter")?null:e.createNewLabel(e.label)},input:function input(n){n.target.composing||(e.label=n.target.value)}}}),e._v(" "),n("svgicon",{staticClass:"new-label__close",attrs:{name:"close"},on:{click:function click(n){return e.reset()}}}),e._v(" "),n("base-button",{staticClass:"new-label__button primary small",attrs:{disabled:!e.label},on:{click:function click(n){return e.createNewLabel(e.label)}}},[e._v("Create")])],1):n("base-button",{staticClass:"new-label__main-button secondary text",on:{click:function click(n){return e.openLabelCreation()}}},[e._v(e._s(e.text))])],1)}),[],!1,null,"f0778682",null);n.default=s.exports;installComponents(s,{BaseButton:t(415).default})}}]);