(window.webpackJsonp=window.webpackJsonp||[]).push([[217,59,85,141,216],{1017:function(e,n,i){var t=i(1185);t.__esModule&&(t=t.default),"string"==typeof t&&(t=[[e.i,t,""]]),t.locals&&(e.exports=t.locals);(0,i(82).default)("02ea5c56",t,!0,{sourceMap:!1})},1184:function(e,n,i){"use strict";i(1017)},1185:function(e,n,i){var t=i(81),s=i(85),o=i(86),a=i(87),r=t((function(e){return e[1]})),c=s(o),h=s(a);r.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+c+') format("woff2"),url('+h+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */[data-v-25084993] .whitespace{background:#fff;border-bottom:5px solid #fff;display:inline;font-size:16px;font-size:1rem;padding-bottom:3px;white-space:pre-line}.highlight[data-v-25084993]{border-radius:2px;cursor:default;font-size:0;line-height:1em;padding:0;position:relative}.highlight.editable[data-v-25084993]{cursor:pointer}.highlight--block[data-v-25084993]{display:block}.highlight--block .highlight__content[data-v-25084993]:after{content:"";height:100%;position:absolute;top:0;width:100%}.highlight__content[data-v-25084993]{display:inline;font-size:16px;font-size:1rem;padding-bottom:1px;white-space:pre-line}.highlight:hover .remove-button[data-v-25084993]{opacity:1;z-index:5}.remove-button[data-v-25084993]{fill:#fff;background:rgba(0,0,0,.87);border-radius:2px;min-width:10px;opacity:0;padding:2px;position:absolute;right:-3px;top:-23px;z-index:-1}',""]),r.locals={},e.exports=r},1306:function(e,n,i){"use strict";i.r(n);i(89),i(30),i(753);var t=i(179),s={props:{span:{type:Object,required:!0},whiteSpace:{type:String},datasetName:{type:String,required:!0},record:{type:Object,required:!0}},data:function data(){return{singleClickDelay:300,doubleClicked:!1,clicked:!1,showTooltip:!1}},computed:{viewSettings:function viewSettings(){return this.datasetName?Object(t.b)(this.datasetName):{}},annotationEnabled:function annotationEnabled(){return"annotate"===this.viewSettings.viewMode},charsBetweenTokens:function charsBetweenTokens(){return this.span.tokens[this.span.tokens.length-1].charsBetweenTokens}},methods:{openTagSelector:function openTagSelector(){var e=this;this.clicked=!0,this.annotationEnabled&&setTimeout((function(){e.doubleClicked||e.$emit("openTagSelector"),e.clicked=!1}),this.singleClickDelay)},removeEntity:function removeEntity(){var e=this;this.doubleClicked=!0,this.annotationEnabled&&(this.$emit("removeEntity"),setTimeout((function(){e.doubleClicked=!1}),this.singleClickDelay))},visualizeToken:function visualizeToken(e,n){var i=e.highlighted?this.$htmlHighlightText(e.text):this.$htmlText(e.text);return"".concat(i).concat(e.charsBetweenTokens&&n+1!==this.span.tokens.length?e.charsBetweenTokens:"")}}},o=(i(1184),i(39)),a=Object(o.a)(s,(function render(){var e=this,n=e._self._c;return n("span",{class:["highlight",e.span.origin,e.annotationEnabled?"editable":null],on:{mouseenter:function mouseenter(n){e.showTooltip=!0},mouseleave:function mouseleave(n){e.showTooltip=!1}}},[e._l(e.span.tokens,(function(i,t){return n("span",{key:t,staticClass:"highlight__content",domProps:{innerHTML:e._s(e.visualizeToken(i,t))},on:{click:e.openTagSelector,dblclick:e.removeEntity}})})),n("span",{staticClass:"whitespace"},[e._v(e._s(e.charsBetweenTokens))]),e._v(" "),e.annotationEnabled&&"annotation"===e.span.origin?n("svgicon",{staticClass:"remove-button",attrs:{width:"11",height:"11",name:"close"},on:{click:e.removeEntity}}):e._e(),e._v(" "),e.showTooltip?n("lazy-text-span-tooltip",{attrs:{span:e.span}}):e._e()],2)}),[],!1,null,"25084993",null);n.default=a.exports},753:function(e,n,i){i(178).register({close:{width:41,height:40,viewBox:"0 0 41 40",data:'<path pid="0" d="M8.922 5.587a2.005 2.005 0 10-2.835 2.835L17.665 20 6.087 31.577a2.005 2.005 0 102.836 2.836L20.5 22.835l11.577 11.578a2.005 2.005 0 002.836-2.836L23.335 20 34.913 8.422a2.005 2.005 0 00-2.835-2.835L20.5 17.165 8.922 5.587z" _fill="#000"/>'}})}}]);