(window.webpackJsonp=window.webpackJsonp||[]).push([[129],{766:function(e,n,i){i(178).register({validate:{width:31,height:31,viewBox:"0 0 31 31",data:'<path pid="0" fill-rule="evenodd" clip-rule="evenodd" d="M15.75.75c-8.284 0-15 6.716-15 15 0 8.284 6.716 15 15 15 8.284 0 15-6.716 15-15 0-8.284-6.716-15-15-15zm-11.826 15c0-6.531 5.295-11.826 11.826-11.826 6.531 0 11.826 5.295 11.826 11.826 0 6.531-5.295 11.826-11.826 11.826-6.531 0-11.826-5.295-11.826-11.826zm19.3-3.698L20.98 9.807l-7.587 7.587-3.794-3.793-2.244 2.244 6.038 6.039 9.832-9.832z" _fill="#000"/>'}})},767:function(e,n,i){i(178).register({discard:{width:16,height:16,viewBox:"0 0 16 16",data:'<path pid="0" fill-rule="evenodd" clip-rule="evenodd" d="M13.303 2.697A7.5 7.5 0 112.697 13.303 7.5 7.5 0 0113.303 2.697zm-1.81 9.975L3.329 4.506a5.835 5.835 0 008.166 8.166zm.632-8.797a5.835 5.835 0 01.547 7.619L4.506 3.328a5.835 5.835 0 017.619.547z" _fill="#000"/>'}})},782:function(e,n,i){"use strict";i.r(n);i(17),i(24),i(67),i(29),i(6),i(766),i(767),i(811),i(812);var t={props:{actions:{type:Array,required:!0,validator:function validator(e){return e.map((function(e){return["validate","discard","clear","reset"].includes(e.id)}))}}},computed:{allowedActions:function allowedActions(){return this.actions.filter((function(e){return e.allow}))}},methods:{onAction:function onAction(e){this.$emit(e)}}},a=(i(853),i(39)),o=Object(a.a)(t,(function render(){var e=this,n=e._self._c;return n("div",{staticClass:"record__actions-buttons"},e._l(e.allowedActions,(function(i){var t=i.id,a=i.name,o=i.active,r=i.disable;return n("span",{key:t},[n("base-button",{class:"record__actions-button--".concat(t),attrs:{disabled:r,active:o&&!r},on:{click:function click(n){return e.onAction(t)}}},[n("svgicon",{attrs:{name:t,width:"14",height:"14"}}),e._v("\n      "+e._s(a)+"\n    ")],1)],1)})),0)}),[],!1,null,"548ee73f",null);n.default=o.exports;installComponents(o,{BaseButton:i(415).default})},790:function(e,n,i){var t=i(854);t.__esModule&&(t=t.default),"string"==typeof t&&(t=[[e.i,t,""]]),t.locals&&(e.exports=t.locals);(0,i(82).default)("743be2cc",t,!0,{sourceMap:!1})},811:function(e,n,i){i(178).register({clear:{width:18,height:18,viewBox:"0 0 18 18",data:'<path pid="0" fill-rule="evenodd" clip-rule="evenodd" d="M1.02 9.845a1.878 1.878 0 000 2.655l3.622 3.622H1.569a.939.939 0 000 1.878h15.023a.939.939 0 000-1.878H8.02l8.933-8.933a1.878 1.878 0 000-2.656L12.97.55a1.878 1.878 0 00-2.656 0L1.019 9.845zm4.06-1.406l-2.733 2.733 3.984 3.984 2.733-2.734-3.983-3.983zM6.41 7.11l3.983 3.983 5.233-5.233-3.983-3.983L6.409 7.11z" _fill="#52A3ED"/>'}})},812:function(e,n,i){i(178).register({reset:{width:16,height:18,viewBox:"0 0 16 18",data:'<path pid="0" d="M.041 0h2.39v3.055a8.364 8.364 0 11-1.24 11.962l1.936-1.415a5.974 5.974 0 10.987-8.823h3.097v2.39H.04V0z" _fill="#000"/>'}})},853:function(e,n,i){"use strict";i(790)},854:function(e,n,i){var t=i(81),a=i(85),o=i(86),r=i(87),s=t((function(e){return e[1]})),c=a(o),d=a(r);s.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+c+') format("woff2"),url('+d+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.record__actions-buttons[data-v-548ee73f]{align-items:center;display:flex;gap:8px;margin-top:32px}.record__actions-button--validate[data-v-548ee73f]{background:#f5f5f5;border:1px solid rgba(0,0,0,.1);color:rgba(0,0,0,.6);padding:7px 8px}.record__actions-button--validate[data-v-548ee73f]:hover{background:#f0f0f0}.record__actions-button--validate .svg-icon[data-v-548ee73f]{color:#60a018;flex-shrink:0}.record__actions-button--validate:active .svg-icon[data-v-548ee73f]{animation:zoom-in-out-548ee73f .2s linear}.record__actions-button--validate[disabled][data-v-548ee73f]{opacity:.4}.record__actions-button--discard[data-v-548ee73f]{background:#f5f5f5;border:1px solid rgba(0,0,0,.1);color:rgba(0,0,0,.6);padding:7px 8px}.record__actions-button--discard[data-v-548ee73f]:hover{background:#f0f0f0}.record__actions-button--discard .svg-icon[data-v-548ee73f]{color:rgba(0,0,0,.6);flex-shrink:0}.record__actions-button--discard:active .svg-icon[data-v-548ee73f]{animation:zoom-in-out-548ee73f .2s linear}.record__actions-button--discard[disabled][data-v-548ee73f]{opacity:.4}.record__actions-button--clear[data-v-548ee73f]{background:#f5f5f5;border:1px solid rgba(0,0,0,.1);color:rgba(0,0,0,.6);padding:7px 8px}.record__actions-button--clear[data-v-548ee73f]:hover{background:#f0f0f0}.record__actions-button--clear .svg-icon[data-v-548ee73f]{color:rgba(0,0,0,.6);flex-shrink:0}.record__actions-button--clear:active .svg-icon[data-v-548ee73f]{animation:zoom-in-out-548ee73f .2s linear}.record__actions-button--clear[disabled][data-v-548ee73f]{opacity:.4}.record__actions-button--reset[data-v-548ee73f]{background:#f5f5f5;border:1px solid rgba(0,0,0,.1);color:rgba(0,0,0,.6);padding:7px 8px}.record__actions-button--reset[data-v-548ee73f]:hover{background:#f0f0f0}.record__actions-button--reset .svg-icon[data-v-548ee73f]{color:rgba(0,0,0,.6);flex-shrink:0}.record__actions-button--reset:active .svg-icon[data-v-548ee73f]{animation:zoom-in-out-548ee73f .2s linear}.record__actions-button--reset[disabled][data-v-548ee73f]{opacity:.4}.record__actions-button--validate[data-v-548ee73f]{color:#60a018}.record__actions-button--validate[active][data-v-548ee73f]{background:#fff;border-color:#60a018;opacity:1}.record__actions-button--discard[active][data-v-548ee73f]{background:#fff;opacity:1}@keyframes zoom-in-out-548ee73f{0%{transform:scale(1)}30%{transform:scale(.8)}to{transform:scale(1)}}',""]),s.locals={},e.exports=s}}]);