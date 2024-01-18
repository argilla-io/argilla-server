(window.webpackJsonp=window.webpackJsonp||[]).push([[186,52],{756:function(e,n,i){var t=i(773);t.__esModule&&(t=t.default),"string"==typeof t&&(t=[[e.i,t,""]]),t.locals&&(e.exports=t.locals);(0,i(82).default)("5554d638",t,!0,{sourceMap:!1})},769:function(e,n,i){"use strict";i.r(n);i(17),i(233);var t=i(68),o={name:"BaseRadioButton",props:{id:{type:String},name:{type:String},model:{type:[String,Number,Boolean,Object]},value:{type:[String,Number,Boolean,Object]},disabled:Boolean,color:{type:String,default:"#3e5cc9"}},model:{prop:"model",event:"change"},computed:{isSelected:function isSelected(){return Object(t.isEqual)(this.model,this.value)},radioClasses:function radioClasses(){return{"--checked":this.isSelected,"--disabled":this.disabled}},cssVars:function cssVars(){return{"--radio-color":this.color}}},methods:{toggleCheck:function toggleCheck(){this.disabled||this.$emit("change",this.value)}}},s=(i(772),i(39)),r=Object(s.a)(o,(function render(){var e=this,n=e._self._c;return n("div",{staticClass:"radio-button",class:[e.radioClasses],on:{click:function click(n){return n.stopPropagation(),e.toggleCheck.apply(null,arguments)}}},[n("div",{staticClass:"radio-button__container",style:e.cssVars},[n("input",e._b({attrs:{type:"radio"}},"input",{id:e.id,name:e.name,disabled:e.disabled,value:e.value,checked:e.isSelected},!1))]),e._v(" "),n("label",{staticClass:"radio-button__label",attrs:{for:e.id},on:{click:function click(n){return n.preventDefault(),e.toggleCheck.apply(null,arguments)}}},[e._t("default")],2)])}),[],!1,null,null,null);n.default=r.exports},772:function(e,n,i){"use strict";i(756)},773:function(e,n,i){var t=i(81),o=i(85),s=i(86),r=i(87),a=t((function(e){return e[1]})),c=o(s),d=o(r);a.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+c+') format("woff2"),url('+d+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.radio-button__container input{clip:rect(0 0 0 0);clip:rect(0,0,0,0);height:1px;margin:-1px;overflow:hidden;padding:0;position:absolute;width:1px}.radio-button{display:flex;gap:8px;margin:16px 16px 16px 0;position:relative;word-break:break-word}.radio-button:not(.--disabled),.radio-button:not(.--disabled) .radio-button__label{cursor:pointer}.radio-button__container{background:#fff;border:1px solid #e6e6e6;border-radius:50%;height:20px;min-width:20px;position:relative;transition:all .2s ease;width:20px}.radio-button__container:after,.radio-button__container:before{content:" ";position:absolute;transition:all .2s ease}.radio-button__container:before{border-radius:50%;height:20px;left:50%;top:50%;transform:translate(-50%,-50%);width:20px;z-index:1}.radio-button__container:after{background:#fff;border-radius:50%;bottom:6px;left:6px;opacity:0;position:absolute;right:6px;top:6px;transform:scale3D(0,0,1)}.radio-button__container:hover{border-color:var(--radio-color);transition:border-color .3s ease-in-out}.radio-button__container:focus{outline:none}.radio-button__label{height:20px;line-height:20px;position:relative}.radio-button.--checked .radio-button__container{background:var(--radio-color);border-color:var(--radio-color)}.radio-button.--checked .radio-button__container:after{opacity:1;transform:scaleX(1);transition:all .3s ease}',""]),a.locals={},e.exports=a},798:function(e,n,i){var t=i(885);t.__esModule&&(t=t.default),"string"==typeof t&&(t=[[e.i,t,""]]),t.locals&&(e.exports=t.locals);(0,i(82).default)("1e42abb5",t,!0,{sourceMap:!1})},884:function(e,n,i){"use strict";i(798)},885:function(e,n,i){var t=i(81),o=i(85),s=i(86),r=i(87),a=t((function(e){return e[1]})),c=o(s),d=o(r);a.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+c+') format("woff2"),url('+d+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.similarity-search[data-v-52507a23]{position:relative}.similarity-search__options[data-v-52507a23]{margin-bottom:2em}.similarity-search__title[data-v-52507a23]{color:rgba(0,0,0,.87);font-weight:500;margin-top:0}',""]),a.locals={},e.exports=a},926:function(e,n,i){"use strict";i.r(n);var t={props:{formattedVectors:{type:Array,required:!0},selectedVector:{type:Object,required:!0}},model:{prop:"selectedVector",event:"vector-change"},computed:{selectedName:{get:function get(){return this.selectedVector},set:function set(e){this.$emit("vector-change",e)}}}},o=(i(884),i(39)),s=Object(o.a)(t,(function render(){var e=this,n=e._self._c;return n("div",{staticClass:"similarity-search__options"},[n("p",{staticClass:"similarity-search__title"},[e._v("Select vector:")]),e._v(" "),e._l(e.formattedVectors,(function(i){return n("base-radio-button",{key:i.vectorName,attrs:{id:i.vectorName,value:i},model:{value:e.selectedName,callback:function callback(n){e.selectedName=n},expression:"selectedName"}},[e._v("\n    "+e._s(i.vectorName)+"\n  ")])}))],2)}),[],!1,null,"52507a23",null);n.default=s.exports;installComponents(s,{BaseRadioButton:i(769).default})}}]);