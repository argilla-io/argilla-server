(window.webpackJsonp=window.webpackJsonp||[]).push([[195],{1021:function(e,n,i){var t=i(1189);t.__esModule&&(t=t.default),"string"==typeof t&&(t=[[e.i,t,""]]),t.locals&&(e.exports=t.locals);(0,i(82).default)("73b3829c",t,!0,{sourceMap:!1})},1188:function(e,n,i){"use strict";i(1021)},1189:function(e,n,i){var t=i(81),s=i(85),o=i(86),r=i(87),a=t((function(e){return e[1]})),c=s(o),l=s(r);a.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+c+') format("woff2"),url('+l+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.selector[data-v-29fe44a8]{margin-bottom:2em;position:relative}.selector__header[data-v-29fe44a8]{align-items:center;border:1px solid #e6e6e6;border-radius:5px;cursor:pointer;display:flex;font-size:13px;font-size:.8125rem;padding:.5em 1em}.selector__header[data-v-29fe44a8]:after{border-color:#212121;border-style:solid;border-width:1px 1px 0 0;content:"";display:inline-block;height:8px;margin-bottom:2px;margin-left:auto;transform:rotate(133deg);transition:all 1.5s ease;width:8px}.selector__body[data-v-29fe44a8]{background:#fff;border:1px solid #e6e6e6;display:block;list-style:none;margin-top:0;padding:1em;position:absolute;top:100%;width:100%;z-index:1}.selector__body a[data-v-29fe44a8]{display:block;outline:none;padding:.5em 0;-webkit-text-decoration:none;text-decoration:none}.selector__body a[data-v-29fe44a8]:hover{font-weight:600}',""]),a.locals={},e.exports=a},1222:function(e,n,i){"use strict";i.r(n);i(17),i(29),i(6);var t={props:{selectedOption:{type:Object,required:!0},options:{type:Array,required:!0}},data:function data(){return{showOptionsSelector:!1}},computed:{filteredOptions:function filteredOptions(){var e=this;return this.options.filter((function(n){return n.name!==e.selectedOption.name}))}},methods:{openSelector:function openSelector(){this.showOptionsSelector=!this.showOptionsSelector},selectOption:function selectOption(e){this.$emit("selectOption",e),this.showOptionsSelector=!1},onClickOutside:function onClickOutside(){this.showOptionsSelector=!1}}},s=(i(1188),i(39)),o=Object(s.a)(t,(function render(){var e=this,n=e._self._c;return n("div",{staticClass:"selector"},[e.filteredOptions.length?n("p",{staticClass:"selector__header",on:{click:e.openSelector}},[e._v("\n    "+e._s(e.selectedOption.name)+"\n  ")]):n("p",{staticClass:"metrics__subtitle"},[e._v(e._s(e.selectedOption.name))]),e._v(" "),n("transition",{attrs:{name:"fade"}},[e.showOptionsSelector?n("ul",{directives:[{name:"click-outside",rawName:"v-click-outside",value:e.onClickOutside,expression:"onClickOutside"}],staticClass:"selector__body"},e._l(e.filteredOptions,(function(i){return n("li",{key:i.id},[n("a",{attrs:{href:"#"},on:{click:function click(n){return n.preventDefault(),e.selectOption(i)}}},[e._v(e._s(i.name))])])})),0):e._e()])],1)}),[],!1,null,"29fe44a8",null);n.default=o.exports}}]);