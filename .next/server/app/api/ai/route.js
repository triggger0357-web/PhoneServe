(()=>{var e={};e.id=700;e.ids=[700];e.modules={846:e=>{"use strict";e.exports=require("next/dist/compiled/next-server/app-page.runtime.prod.js")},3033:e=>{"use strict";e.exports=require("next/dist/server/app-render/work-unit-async-storage.external.js")},4772:(e,r,t)=>{"use strict";t.r(r);t.d(r,{patchFetch:()=>h,routeModule:()=>d,serverHooks:()=>l,workAsyncStorage:()=>p,workUnitAsyncStorage:()=>c});var s={};t.r(s);t.d(s,{POST:()=>i});var a=t(6559);var o=t(8088);var n=t(7719);async function i(e){const{prompt:r}=await e.json();const t=`AI draft for: ${r}

Suggested page copy:
- Headline: Launch your sovereign node network.
- Subheadline: Monitor nodes, capture leads, and manage access from one dashboard.
- CTA: Launch PhoneServe.

Suggested admin action:
- Review account status and link billing.
- Check node health.
- Publish if content looks good.`;return Response.json({text:t})};const u="";const d=new a.AppRouteRouteModule({definition:{kind:o.RouteKind.APP_ROUTE,page:"/api/ai/route",pathname:"/api/ai",filename:"route",bundlePath:"app/api/ai/route"},resolvedPagePath:"/data/data/com.termux/files/home/PhoneServe/app/api/ai/route.ts",nextConfigOutput:u,userland:s});const{workAsyncStorage:p,workUnitAsyncStorage:c,serverHooks:l}=d;function h(){return(0,n.patchFetch)({workAsyncStorage:p,workUnitAsyncStorage:c})}},4870:e=>{"use strict";e.exports=require("next/dist/compiled/next-server/app-route.runtime.prod.js")},6487:()=>{},6559:(e,r,t)=>{"use strict";if(false){}else{if(false){}else{if(false){}else{if(false){}else{e.exports=t(4870)}}}}},8335:()=>{},9294:e=>{"use strict";e.exports=require("next/dist/server/app-render/work-async-storage.external.js")}};var r=require("../../../webpack-runtime.js");r.C(e);var t=e=>r(r.s=e);var s=r.X(0,[719],()=>t(4772));module.exports=s})();