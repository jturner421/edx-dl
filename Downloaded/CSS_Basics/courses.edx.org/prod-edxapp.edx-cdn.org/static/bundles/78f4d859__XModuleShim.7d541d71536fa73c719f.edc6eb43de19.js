!function(o,t){for(var e in t)o[e]=t[e]}(window,webpackJsonp([44],{"./common/lib/xmodule/xmodule/js/src/xmodule.js":function(o,t,e){(function(t,e){(function(){(function(){"use strict";var o={};o.Descriptor=function(){var o=function(o){this.element=o,this.update=t.bind(this.update,this)};return o.prototype.onUpdate=function(o){this.callbacks||(this.callbacks=[]),this.callbacks.push(o)},o.prototype.update=function(){var o,t;o=this.save(),t=this.callbacks,t.length,e.each(t,function(t,e){e(o)})},o.prototype.save=function(){return{}},o}(),this.XBlockToXModuleShim=function(o,t,n){var i,l;if(n&&(i=n["xmodule-type"]),i||(i=e(t).data("type")),"None"!==i)try{return l=new window[i](t),e(t).hasClass("xmodule_edit")&&e(document).trigger("XModule.loaded.edit",[t,l]),e(t).hasClass("xmodule_display")&&e(document).trigger("XModule.loaded.display",[t,l]),l}catch(o){console.error("Unable to load "+i+": "+o.message)}},this.XModule=o}).call(this)}).call(window),o.exports=window.XModule}).call(t,e(1),e(0))}},["./common/lib/xmodule/xmodule/js/src/xmodule.js"]));
/*!
* AerWebCopy Engine [version 6.1.1]
* Copyright Aeroson Systems & Co.
* File mirrored from https://prod-edxapp.edx-cdn.org/static/bundles/XModuleShim.7d541d71536fa73c719f.edc6eb43de19.js
* At UTC time: 2020-01-05 02:12:50.242228
*/
