/* LEA read-only UI. Original logo: Notruf Niederösterreich; see ATTRIBUTION.md. */
const LEA_LOGO = "data:image/svg+xml;base64,PHN2ZyBmaWxsPSJub25lIiBoZWlnaHQ9IjM1IiB2aWV3Qm94PSIwIDAgNjAgMzUiIHdpZHRoPSI2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8ZyBjbGlwLXBhdGg9InVybCgjY2xpcDBfMjcyOV8zNTQpIj4KICAgIDxwYXRoCiAgICAgIGQ9Ik0yNC4xNjY2IDIxLjEzNjZIMzAuNzgyMkMzMy4xNjMgMjEuMjc5OCAzNC43MDg2IDIzLjQwMTIgMzMuMzQyMSAyNS4zNDI1QzMzLjIwOTggMjUuNTMwNiAzMy4wNDQ4IDI1LjY5NDggMzIuODU5MyAyNS44MzQxQzMyLjg1ODEgMjUuODM1MiAzMi44NTY5IDI1LjgzNTggMzIuODU1NyAyNS44MzY5QzMyLjE5MjEgMjYuMzA1MiAzMS4zODkxIDI2LjU1MTggMzAuNTY4IDI2LjU1MThIMjQuMTY2NlYyOS40MzkzSDM0LjI2NUMzNS4zNjY1IDI5LjQzOTMgMzUuOTIzIDI4LjQ4NDYgMzYuMzgxOSAyNy43OTkyQzM5LjIzNzMgMjMuNTMwOCA0MS41MTQ1IDE4Ljg1ODMgNDQuMTMxNyAxNC40MzE4QzQ0LjQ1ODggMTMuODc4MyA0NC45MDcxIDEzLjM5NyA0NS40NjA4IDEzLjA1MzJDNDcuMDk2IDEyLjAzNzYgNDguOTQ1OSAxMi40OTc5IDUwLjE2MzggMTQuMzYyNUM1My41NDE5IDE5LjUzNTcgNTYuMjc3MyAyNS40MTA3IDU5LjU2NTIgMzAuNjkwN0M2MC4yODY4IDMxLjg0ODkgNjAuMTAxMyAzMy4zNTYgNTkuMDgyNCAzNC4yOEM1OC42NjggMzQuNjU1NyA1OC4xNDY2IDM0LjkxMzEgNTcuNTYxMyAzNC45NzM5QzU1Ljg2NyAzNS4xNTAxIDU0Ljk1IDM0LjQ0NzEgNTQuMTMxOCAzMy4xMjk4QzUxLjg2MjIgMjkuNDc2OCA0OS45Nzg5IDI1LjU2OTIgNDcuNzMxNSAyMS44OTg2QzQ3LjU1NDIgMjEuNjA5NCA0Ny4zNjY5IDIxLjIxNDQgNDcuMDkxOSAyMS4wMTcyTDQxLjU5MjMgMzAuNzc4MkM0MS41NTg0IDMwLjgyODIgNDEuNTIzOCAzMC44NzgyIDQxLjQ4OTMgMzAuOTI3MUMzOS42OTY3IDMzLjQ3OTMgMzYuNjk2MSAzNC45Nzg1IDMzLjUxNDcgMzQuOTc4NUgyMC44Nzg3QzIwLjgxMDggMzQuOTcyOCAyMC43NDM1IDM0Ljk2NDMgMjAuNjc2MiAzNC45NTM1QzE5LjMyMDggMzQuNzM3NSAxOC4zNDM0IDMzLjU3MDIgMTguMzQyOCAzMi4yMzY1TDE4LjMzODEgMTQuOTM1NEMxOC4zOTAyIDE0LjEyNzIgMTguODYxMyAxMy40NzY2IDE5LjUxNTYgMTMuMDYwNkMyMC4wMDc4IDEyLjc0NzQgMjAuNTg5IDEyLjU5NCAyMS4xNzcyIDEyLjU5NEMyNS41NjQyIDEyLjU5NCAzMi45MDc4IDEyLjU4OTQgMzIuOTA3OCAxMi41ODk0QzM0LjY4MDUgMTIuNzQ2OSAzNS42OTgzIDE0LjI1NjIgMzUuNzE4MiAxNS43MTczQzM1LjczNzUgMTcuMTUxMSAzNC40ODY4IDE4LjI5MzQgMzMuMDEwMyAxOC4yNDk2QzMyLjk2MTEgMTguMjQ3OSAzMi45MjMxIDE4LjI0OTYgMzIuOTAyNiAxOC4yNDk2QzMyLjkwMjYgMTguMjQ5NiAyNC4xNjcyIDE4LjIwNjQgMjQuMTY3MiAxOC4yNDk2VjIxLjEzNzdMMjQuMTY2NiAyMS4xMzY2WiIKICAgICAgZmlsbD0id2hpdGUiLz4KICAgIDxwYXRoCiAgICAgIGQ9Ik01Ljk1MTk4IDI5LjQzODZIMTQuMDI4NEMxNS4yNTU2IDI5LjQzODYgMTYuMzUzNiAzMC4xOTYyIDE2Ljc0MjIgMzEuMzI2NUMxNi43NDQ1IDMxLjMzMzMgMTYuNzQ2OCAzMS4zNDAxIDE2Ljc0OTIgMzEuMzQ3QzE3LjM0NDQgMzMuMTA5OCAxNS45NTAzIDM0LjkxNyAxNC4wNDAxIDM0LjkyNDlMMi44MDI3NyAzNC45NzIxQzIuMjkxMjYgMzQuOTc0NCAxLjc4MzI3IDM0Ljg1MjIgMS4zNDY2OCAzNC41OTMxQzAuNTQ2MDU5IDM0LjExODUgMC4wODc4MTIgMzMuMjg4OCAwLjAwMDYxMDM1MiAzMi4yNzA0VjE1LjQxNzJDMC4wOTAxNTMgMTIuOTI1MiAzLjMzMzU5IDExLjY0OTkgNS4xNDYwOSAxMy40MzcyQzUuMjA5ODggMTMuNTAwMyA1LjI5MTgyIDEzLjYyNTMgNS4zNzk2MSAxMy43NzgyQzUuNzYwMDIgMTQuNDQyIDUuOTUyNTYgMTUuMTkyMSA1Ljk1MjU2IDE1Ljk1MTlWMjkuNDM4Nkg1Ljk1MTk4WiIKICAgICAgZmlsbD0id2hpdGUiLz4KICAgIDxwYXRoCiAgICAgIGQ9Ik00Ny4xMjU4IDBDNDcuMTI1OCAwIDQ3LjEyMzQgMCA0Ny4xMjIyIDBDNDcuMTIxMSAwIDQ3LjExOTkgMCA0Ny4xMTg3IDBDNDQuMzQgMC4wMDM0MDk3NiA0MS41NjEyIDAuNTE4ODUxIDM4LjkxMyAxLjU1MDNDMzcuODcxMyAxLjk1NjA2IDM3LjUwNzIgMy4yMTI1NiAzOC4xODAzIDQuMDg0ODlDMzguNjM5NyA0LjY4MDQ2IDM5LjQ1MDggNC45MDAzOSA0MC4xNjQzIDQuNjI5MzFDNDIuNDEzNCAzLjc3NTE3IDQ0Ljc2NjYgMy4zNDM4MyA0Ny4xMjE3IDMuMzQwOTlDNDkuNDc2NyAzLjM0MzgzIDUxLjgzIDMuNzc1MTcgNTQuMDc5MSA0LjYyOTMxQzU0Ljc5MjUgNC45MDAzOSA1NS42MDM2IDQuNjgwNDYgNTYuMDYzIDQuMDg0ODlDNTYuNzM2MSAzLjIxMjU2IDU2LjM3MjEgMS45NTYwNiA1NS4zMzAzIDEuNTUwM0M1Mi42ODMzIDAuNTE4ODUxIDQ5LjkwNDUgMC4wMDM5NzgwNSA0Ny4xMjU4IDBaIgogICAgICBmaWxsPSJ3aGl0ZSIvPgogICAgPHBhdGgKICAgICAgZD0iTTQ3LjEyNTcgNS43Njk5QzQ3LjEyNTcgNS43Njk5IDQ3LjEyMzQgNS43Njk5IDQ3LjEyMjIgNS43Njk5QzQ3LjEyMSA1Ljc2OTkgNDcuMTE5OSA1Ljc2OTkgNDcuMTE4NyA1Ljc2OTlDNDUuNTYzNyA1Ljc3MTYgNDQuMDA3IDYuMDA0MDMgNDIuNTA3NiA2LjQ1MDE0QzQxLjM3NDUgNi43ODcxNCA0MC45MjI3IDguMTEwMTMgNDEuNjMzMiA5LjAzMTMzTDQxLjcxNDUgOS4xMzcwM0M0Mi4xNDQxIDkuNjkzMzkgNDIuODgyNyA5LjkxOSA0My41NzA0IDkuNzI1NzhDNDQuNzI4NiA5LjQwMDE1IDQ1LjkyNjYgOS4yMzE5NCA0Ny4xMjIyIDkuMjMxMzdDNDguMzE3OSA5LjIzMjUgNDkuNTE1OSA5LjQwMDcyIDUwLjY3NDEgOS43MjU3OEM1MS4zNjE3IDkuOTE5IDUyLjEwMDMgOS42OTMzOSA1Mi41Mjk5IDkuMTM3MDNMNTIuNjExMiA5LjAzMTMzQzUzLjMyMTcgOC4xMTAxMyA1Mi44Njk5IDYuNzg3MTQgNTEuNzM2OSA2LjQ1MDE0QzUwLjIzNjkgNi4wMDQwMyA0OC42ODAxIDUuNzcxNiA0Ny4xMjU3IDUuNzcwNDdWNS43Njk5WiIKICAgICAgZmlsbD0id2hpdGUiLz4KICAgIDxwYXRoCiAgICAgIGQ9Ik00Ny4xMTk0IDMzLjkxMjJDNDguODI5NSAzMy45MTIyIDUwLjIxNTkgMzIuNTY2IDUwLjIxNTkgMzAuOTA1NEM1MC4yMTU5IDI5LjI0NDggNDguODI5NSAyNy44OTg2IDQ3LjExOTQgMjcuODk4NkM0NS40MDkyIDI3Ljg5ODYgNDQuMDIyOCAyOS4yNDQ4IDQ0LjAyMjggMzAuOTA1NEM0NC4wMjI4IDMyLjU2NiA0NS40MDkyIDMzLjkxMjIgNDcuMTE5NCAzMy45MTIyWiIKICAgICAgZmlsbD0id2hpdGUiLz4KICA8L2c+CiAgPGRlZnM+CiAgICA8Y2xpcFBhdGggaWQ9ImNsaXAwXzI3MjlfMzU0Ij4KICAgICAgPHJlY3QgZmlsbD0id2hpdGUiIGhlaWdodD0iMzUiIHdpZHRoPSI2MCIvPgogICAgPC9jbGlwUGF0aD4KICA8L2RlZnM+Cjwvc3ZnPgo=";
const LEA_LABELS = {alarm:"Meldung",information:"Info-Meldung",cancellation:"Storno",message:"Nachricht",unknown:"Meldung"};
const leaEscape = value => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const leaTime = value => {
  if (!value) return "Zeit unbekannt";
  const date = new Date(value);
  return Number.isNaN(date.valueOf()) ? "Zeit unbekannt" : new Intl.DateTimeFormat("de-AT", {day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"}).format(date);
};
const leaCoordinates = row => Number.isFinite(row?.latitude) && Number.isFinite(row?.longitude) && Math.abs(row.latitude)<=90 && Math.abs(row.longitude)<=180;

class LeaNoeCard extends HTMLElement {
  constructor() {
    super(); this.attachShadow({mode:"open"});
    this._config={}; this._tab="meldungen"; this._query=""; this._selected=null;
    this._data=null; this._loading=false; this._generation=0; this._nextProbe=0;
    this._detailOpen=false; this._mapConsentFor=null;
    this._mount();
  }
  setConfig(config) {
    this._config={...config};
    if(config.account_entry_id && typeof config.account_entry_id!=="string") throw new Error("account_entry_id muss eine Zeichenfolge sein");
    this._render();
  }
  set hass(hass) {
    this._hass=hass;
    const signature=Object.values(hass.states || {}).filter(s=>s.entity_id?.includes("lea_bos_mobil")).map(s=>s.last_updated).join("|");
    if (signature!==this._signature) { this._signature=signature; this._load(); }
    else if (!this._data) this._load();
  }
  get hass() { return this._hass; }
  connectedCallback() {
    this._timer ??= setInterval(()=>{ if(!document.hidden) this._load(); },15000);
    this._load();
  }
  disconnectedCallback() { clearInterval(this._timer); this._timer=null; this._generation++; this.shadowRoot.querySelectorAll("audio").forEach(a=>a.pause()); }
  getCardSize() { return 12; }
  getGridOptions() { return {columns:"full",rows:"auto",min_rows:8}; }
  static getStubConfig() { return {theme:"dark"}; }
  async _load() {
    if (!this._hass || this._loading || !this.isConnected) return;
    const generation=this._generation; this._loading=true;
    try {
      if (Date.now()<this._nextProbe) { this._legacy(); return; }
      const data=await this._hass.callWS({type:"lea_noe/get_notifications"});
      if (generation!==this._generation) return;
      if (!Array.isArray(data?.accounts)) throw new Error("invalid_response");
      this._data=data; this._fallback=false; this._error="";
    } catch (error) {
      if (generation!==this._generation) return;
      this._nextProbe=Date.now()+60000;
      this._legacy();
    } finally { this._loading=false; if(generation===this._generation) this._render(); }
  }
  _legacy() {
    const states=Object.values(this._hass.states || {});
    const belongs = s => s.entity_id?.includes("lea_bos_mobil") || /LEA BOS mobil/i.test(s.attributes?.friendly_name || "");
    const latest=this._config.entity ? this._hass.states[this._config.entity] : states.find(s=>s.entity_id?.startsWith("sensor.") && belongs(s) && (/letzte_meldung$|latest_notification$/.test(s.entity_id) || Object.hasOwn(s.attributes || {},"meldungs_id")));
    const fetched=states.find(s=>belongs(s) && /letzter_erfolgreicher_abruf$|last_successful_fetch$|last_fetch$/.test(s.entity_id));
    const count=states.find(s=>belongs(s) && /meldungen_im_abruffenster$|inbox_count$/.test(s.entity_id));
    if (!latest) { this._data={accounts:[]}; this._fallback=true; this._error="Noch kein LEA-Zugang verfügbar"; return; }
    const attrs=latest.attributes || {};
    this._data={accounts:[{entry_id:"legacy",title:"LEA BOS mobil",available:!["unavailable","unknown"].includes(latest.state),include_details:Object.hasOwn(attrs,"nachricht"),fetched_at:fetched?.state,total:count?.state,notifications:attrs.meldungs_id ? [{...attrs}] : []}]};
    this._fallback=true; this._error="";
  }
  _account() {
    const accounts=this._data?.accounts || [];
    return accounts.find(a=>a.entry_id===this._config.account_entry_id) || accounts[0];
  }
  _rows() { return (this._account()?.notifications || []).filter(row=>row && typeof row==="object"); }
  _mount() {
    this.shadowRoot.innerHTML=`<style>
      :host{display:block;--blue:#005A9A;--yellow:#ffd900;--ink:#f2f2f7;--surface:rgba(255,255,255,.09);--line:rgba(255,255,255,.12);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink)}
      *{box-sizing:border-box}button,input,select{font:inherit}button{cursor:pointer}button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #ffd900;outline-offset:3px}
      .app{min-height:720px;background:radial-gradient(ellipse 78% 45% at 110% -12%,#a91a24 0,transparent 95%),#101012;border-radius:18px;overflow:hidden;border:1px solid var(--line);position:relative}
      :host([panel]) .app{height:100dvh;min-height:560px;border:0;border-radius:0;display:flex;flex-direction:column}
      .top{background:#005A9A;min-height:86px;padding:18px 28px;display:flex;gap:19px;align-items:center}.logo{width:92px;height:54px;object-fit:contain}.brand{flex:1;min-width:0}.brand strong{font-size:19px;font-weight:700;letter-spacing:.15px}.brand small{display:block;margin-top:5px;color:#d5e7f2;font-size:12px}.read{font-size:10px;letter-spacing:1.25px;text-transform:uppercase;color:#fff;border:1px solid #ffffff45;padding:8px 10px;border-radius:8px;white-space:nowrap}
      .menu{display:none;background:transparent;border:0;color:#fff;font-size:25px;padding:8px}:host([panel]) .menu{display:block}
      .intro{padding:26px 30px 0;display:flex;gap:15px;justify-content:space-between;align-items:center}.intro h1{font-size:29px;letter-spacing:-.8px;margin:0 0 7px;font-weight:700}.sub{font-size:12px;color:#a7acb8}.connection{display:flex;align-items:center;gap:7px;font-size:12px;color:#c4c8d1}.dot{width:7px;height:7px;background:#72b845;border-radius:50%}.dot.bad{background:#f5a244}.controls{display:flex;align-items:center;gap:16px;padding:19px 30px 20px;border-bottom:1px solid var(--line)}.tabs{display:flex;gap:5px;background:#ffffff09;padding:4px;border-radius:11px;flex-shrink:0}.tab{border:0;color:#afb7c3;background:transparent;padding:10px 16px;border-radius:8px;font-size:12px}.tab.active{background:#005A9A;color:#fff;box-shadow:0 2px 7px #0003}.search{margin-left:auto;max-width:310px;flex:1;min-width:100px}.search input{width:100%;border-radius:10px;border:1px solid var(--line);background:#ffffff08;color:var(--ink);padding:12px 14px;font-size:12px}.search input::placeholder{color:#8d95a4}
      .content{padding:22px 30px 28px;min-height:460px;flex:1;overflow:auto}.layout{display:grid;grid-template-columns:minmax(270px,.9fr) minmax(340px,1.3fr);gap:23px;align-items:start}.list{display:grid;gap:12px}.caption{display:flex;justify-content:space-between;align-items:center;color:#a4acb9;font-size:11px;padding:0 0 4px}.notice{margin-bottom:17px;border:1px solid #b886224d;border-radius:10px;background:#d99a1610;color:#e1c99a;padding:12px 14px;font-size:12px;line-height:1.65}.notice a{color:inherit}.row{width:100%;padding:17px;text-align:left;color:var(--ink);border:1px solid var(--line);border-left:4px solid #b93e40;border-radius:12px;background:var(--surface);transition:background .15s,border-color .15s}.row:hover{background:#ffffff14}.row.selected{background:#005a9a25;border-color:#368ec7;border-left-color:#43a4df}.row.information{border-left-color:#539bc4}.row.cancellation{border-left-color:#d9aa47}.row.message{border-left-color:#9a87c5}.row.unknown{border-left-color:#7b828c}.row-top{display:flex;gap:10px;justify-content:space-between;align-items:center;margin-bottom:13px}.chip{display:inline-block;background:#9b3039;color:#fff;border-radius:6px;padding:5px 9px;min-width:35px;font-size:11px;font-weight:700;white-space:nowrap}.information .chip{background:#235c7c}.cancellation .chip{background:#755a22}.message .chip{background:#554373}.unknown .chip{background:#545962}.date{font-size:10px;color:#9ba3b2;text-align:right}.row h3{font-size:15px;line-height:1.45;margin:0 0 8px;font-weight:650;overflow-wrap:anywhere}.place{font-size:11px;color:#a8b0bc;display:block;line-height:1.5;overflow-wrap:anywhere}.row-bottom{display:flex;justify-content:space-between;align-items:center;margin-top:16px;color:#98a3b4;font-size:10px}.arrow{color:#68b5e9;font-size:17px}
      .detail{padding:23px 25px;border-radius:15px;border:1px solid var(--line);background:#191b20;box-shadow:0 4px 20px #0002;min-height:355px}.detail h2{font-size:22px;line-height:1.35;letter-spacing:-.35px;margin:16px 0 18px;overflow-wrap:anywhere}.detail .kicker{display:flex;align-items:center;justify-content:space-between;gap:8px}.detail .kicker small{color:#99a4b5;font-size:11px}.meta{display:grid;grid-template-columns:1fr 1fr;gap:19px 22px;padding-bottom:24px;border-bottom:1px solid var(--line)}.meta label{display:block;color:#969fae;font-size:10px;text-transform:uppercase;letter-spacing:.6px;margin-bottom:7px}.meta span{font-size:12px;overflow-wrap:anywhere}.message-body{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px;line-height:1.8;margin:21px 0 0;color:#d5dae2}.locked{color:#9ea8b7;font-size:12px;line-height:1.8;margin:21px 0 0}.locked a{color:#72b9eb}.detail-footer{font-size:10px;color:#949caa;display:flex;align-items:center;gap:7px;margin-top:24px}.back{display:none;background:none;border:0;color:#74b9e7;margin:0 0 18px;padding:0;font-size:12px}
      .empty{padding:64px 25px;text-align:center;border:1px dashed #ffffff26;border-radius:15px;grid-column:1/-1;color:#aab2c1}.empty .symbol{font-size:34px;color:#568bac;margin-bottom:15px}.empty h2{color:var(--ink);font-size:18px;font-weight:600;margin:8px 0}.empty p{font-size:12px;line-height:1.8;margin:0 auto;max-width:380px}.empty a{color:#72b9eb}
      .map{width:100%;height:380px;border:0;border-radius:10px;margin-top:18px;background:#242a32}.map-button{background:#005A9A;border:0;border-radius:9px;color:#fff;padding:12px 17px;margin-top:16px;font-size:12px}.privacy{font-size:11px;color:#9ca8b8;line-height:1.7;margin-top:13px}.status-card{max-width:720px;margin:auto}.status-line{display:flex;justify-content:space-between;gap:16px;padding:17px 0;border-bottom:1px solid var(--line);font-size:12px}.status-line span:first-child{color:#9ba5b5}.status-line span:last-child{text-align:right}.account{border:1px solid var(--line);border-radius:8px;background:#20242b;color:var(--ink);padding:7px;font-size:11px}.bottom{display:flex;justify-content:space-between;gap:15px;padding:13px 30px;border-top:1px solid var(--line);font-size:10px;color:#8e98aa;background:#141518}.bottom span:first-child{color:#a8b0be}.bottom strong{color:#bfc9d7;font-weight:500}
      :host([light]){--ink:#001D32;--surface:rgba(255,255,255,.95);--line:#dce2e9}:host([light]) .app{background:radial-gradient(ellipse 85% 65% at 110% -10%,#dfc6cb,transparent),#eff2f6}:host([light]) .top{color:#fff}:host([light]) .detail{background:#fff}:host([light]) .sub,:host([light]) .connection,:host([light]) .date,:host([light]) .place,:host([light]) .row-bottom,:host([light]) .locked,:host([light]) .meta label,:host([light]) .privacy{color:#65758a}:host([light]) .message-body{color:#34485e}:host([light]) .bottom{background:#e7ecf2;color:#63728a}:host([light]) .bottom span:first-child,:host([light]) .bottom strong{color:#344b62}:host([light]) .tab{color:#526780}:host([light]) .tab.active{color:#fff}:host([light]) .tabs{background:#dfe6ed}:host([light]) .row.selected{background:#e2f0f9}:host([light]) .account{background:#fff}:host([light]) .notice{color:#705a2a}
      @media(max-width:760px){.layout{grid-template-columns:1fr}.top{padding:15px 18px;gap:12px}.logo{width:74px;height:44px}.brand strong{font-size:16px}.brand small{font-size:10px}.read{font-size:8px;letter-spacing:.8px;padding:7px}.intro{padding:22px 18px 0;align-items:flex-start}.intro h1{font-size:25px}.connection{font-size:10px;padding-top:3px}.controls{padding:16px 18px;gap:12px;flex-wrap:wrap}.tabs{flex:1}.tab{flex:1;padding:10px 12px}.search{max-width:none;flex-basis:100%;margin:0}.content{padding:18px}.detail{padding:20px}.layout:not(.details-open) .detail{display:none}.layout.details-open .list{display:none}.back{display:block}.bottom{padding:13px 18px}.app{border-radius:12px;min-height:680px}:host([panel]) .app{min-height:100dvh}.meta{gap:20px 15px}.read{display:none}}
      .sound-list{display:grid;gap:16px;margin-top:20px}.sound-item{border-top:1px solid var(--line);padding-top:15px}.sound-item label{display:block;font-size:13px;margin-bottom:9px}.sound-item small{color:#929eaf}.sound-item audio{width:100%;height:36px}.tabs{max-width:100%;overflow-x:auto}.tab{white-space:nowrap}a.map-button{display:inline-block;text-decoration:none}@media(prefers-reduced-motion:reduce){*{transition:none!important}}
    </style><div class="app"><header class="top"><button class="menu" aria-label="Home-Assistant-Menü öffnen">☰</button><img class="logo" alt="LEA" src="${LEA_LOGO}"><div class="brand"><strong>Leitstellen &amp; Einsatzorganisationen</strong><small>Persönliche Einsatzinformationen</small></div><span class="read">Nur lesen</span></header><div class="intro"><div><h1>Meldungen</h1><div class="sub">Deine persönliche LEA-Übersicht</div></div><div class="connection"></div></div><div class="controls"><nav class="tabs" aria-label="LEA-Ansicht"><button class="tab active" data-tab="meldungen">Meldungen</button><button class="tab" data-tab="karte">Karte</button><button class="tab" data-tab="alarmtoene">Alarmtöne</button><button class="tab" data-tab="verbindung">Verbindung</button></nav><div class="search"><input type="search" aria-label="Meldungen durchsuchen" placeholder="Meldungen durchsuchen …"></div><div class="account-slot"></div></div><main class="content" aria-live="polite"></main><footer class="bottom"><span>Home Assistant · <strong>LEA</strong></span><span>Inoffizielle Leseansicht</span></footer></div>`;
    this.shadowRoot.querySelector(".menu").addEventListener("click",()=>this.dispatchEvent(new CustomEvent("hass-toggle-menu",{bubbles:true,composed:true})));
    this.shadowRoot.querySelector("input").addEventListener("input",event=>{this._query=event.target.value;this._renderContent();});
    this.shadowRoot.addEventListener("click",event=>{
      const target=event.target.closest("button"); if(!target) return;
      if(target.dataset.tab){this.shadowRoot.querySelectorAll("audio").forEach(a=>a.pause());this._tab=target.dataset.tab;this._render();}
      if(target.dataset.audioAction){
        const entity=this._account()?.audio?.[target.dataset.audioAction];
        if(entity){
          target.disabled=true;
          this._hass.callService("button","press",{entity_id:entity}).then(()=>{
            const result=this.shadowRoot.querySelector(".audio-result");
            if(result) result.textContent=target.dataset.audioAction==="test_entity"?"Wiedergabebefehl an die konfigurierten Geräte gesendet.":"Stoppbefehl gesendet.";
          }).catch(error=>{
            const result=this.shadowRoot.querySelector(".audio-result");
            if(result) result.textContent=error?.message || "Wiedergabebefehl fehlgeschlagen. Bitte die Integrationseinstellungen prüfen.";
          }).finally(()=>{target.disabled=false;});
        }
      }
      if(target.dataset.id){this._selected=target.dataset.id;this._detailOpen=true;this._renderContent();}
      if(target.dataset.action==="back"){this._detailOpen=false;this._renderContent();}
      if(target.dataset.action==="load-map"){this._mapConsentFor=this._selected;this._renderContent();}
    });
  }
  _render() {
    const dark=this._config.theme==="dark" || (this._config.theme!=="light" && this._hass?.themes?.darkMode!==false);
    this.toggleAttribute("light",!dark);
    const account=this._account();
    this.shadowRoot.querySelector(".connection").innerHTML=`<span class="dot ${account?.available ? "" : "bad"}"></span>${account?.available ? "Verbunden" : account ? "Verbindung unterbrochen" : "Warte auf Zugang"}`;
    this.shadowRoot.querySelector("h1").textContent={meldungen:"Meldungen",karte:"Einsatzkarte",verbindung:"Verbindung",alarmtoene:"HA-Alarmtöne"}[this._tab];
    this.shadowRoot.querySelectorAll(".tab").forEach(button=>{button.classList.toggle("active",button.dataset.tab===this._tab);button.setAttribute("aria-current",button.dataset.tab===this._tab ? "page" : "false");});
    this.shadowRoot.querySelector(".search").hidden=this._tab!=="meldungen";
    const slot=this.shadowRoot.querySelector(".account-slot"), accounts=this._data?.accounts || [];
    if(accounts.length>1){slot.innerHTML=`<select class="account" aria-label="LEA-Zugang auswählen">${accounts.map((a,index)=>`<option value="${leaEscape(a.entry_id)}" ${a===account?"selected":""}>${leaEscape(a.title)} ${index+1}</option>`).join("")}</select>`;slot.querySelector("select").addEventListener("change",e=>{this._config.account_entry_id=e.target.value;this._selected=null;this._render();});}else slot.replaceChildren();
    this._renderContent();
  }
  _renderContent() {
    const main=this.shadowRoot.querySelector("main"), account=this._account(), rows=this._rows();
    const contentSignature=JSON.stringify([this._tab,this._query,this._selected,this._detailOpen,this._mapConsentFor,this._fallback,account ? {...account,fetched_at:(this._tab==="alarmtoene" || this._tab==="karte" && account.available) ? null : account.fetched_at} : null]);
    if(contentSignature===this._contentSignature) return;
    this._contentSignature=contentSignature;
    if(!account){main.innerHTML=`<div class="empty"><div class="symbol">◇</div><h2>${this._data ? leaEscape(this._error || "Kein LEA-Zugang geladen") : "LEA wird geladen"}</h2><p>Die Ansicht zeigt die Meldungen deiner Home-Assistant-Integration.<br><a href="/config/integrations/integration/lea_noe">LEA-Integration öffnen</a></p></div>`;return;}
    let notice=!account.available ? `<div class="notice">Die LEA-Integration liefert derzeit keine aktuellen Daten.${account.fetched_at ? ` Letzter bekannter Abruf: ${leaEscape(leaTime(account.fetched_at))}.` : " Es liegt noch kein erfolgreicher Abruf vor."}</div>` : "";
    if(this._fallback) notice+=`<div class="notice">Ansicht der zuletzt abrufbaren Meldung. Für die vollständige Meldungsliste die LEA-Integration aktualisieren.</div>`;
    if(this._tab==="alarmtoene") {main.innerHTML=notice+this._sounds(account);return;}
    if(this._tab==="verbindung") {main.innerHTML=notice+`<section class="detail status-card"><h2>LEA-Verbindung</h2>${[["Status",account.available?"Verbunden":"Nicht erreichbar"],["Datenstand",leaTime(account.fetched_at)],["Abrufbare Meldungen",String(account.total ?? rows.length)],["Zugriff","Ausschließlich lesen"],["Meldungstext und Ort",account.include_details?"Aktiviert":"Ausgeblendet"],["Oberfläche","LEA-Ansicht · 0.3.0"]].map(([key,value])=>`<div class="status-line"><span>${leaEscape(key)}</span><span>${leaEscape(value)}</span></div>`).join("")}<p class="privacy">Ein fehlender oder alter Datenstand ist keine Entwarnung. Die reguläre Alarmierung erfolgt weiterhin über LEA.</p></section>`;return;}
    if(!rows.some(row=>row.meldungs_id===this._selected)) this._selected=rows[0]?.meldungs_id ?? null;
    const selected=rows.find(row=>row.meldungs_id===this._selected);
    if(this._tab==="karte"){main.innerHTML=notice+(selected?this._map(selected,account):this._empty("Noch keine Einsatzkarte","Eine Karte ist verfügbar, sobald eine Meldung mit einem Einsatzort vorliegt."));this._attachMap(selected);return;}
    const q=this._query.trim().toLocaleLowerCase("de-AT");
    const filtered=rows.filter(row=>[row.meldebild,row.nachricht,row.einsatznummer,row.alarmstufe,row.einsatzart,row.einsatzort].some(value=>String(value ?? "").toLocaleLowerCase("de-AT").includes(q)));
    if(!rows.length){main.innerHTML=notice+this._empty(account.available?"Keine Meldungen im Abruffenster":"Meldungen derzeit nicht verfügbar",account.available?"Sobald eine persönliche Meldung abgerufen wurde, erscheint sie hier. Die reguläre Alarmierung erfolgt weiterhin über die LEA-App.":"Der Meldungsstand kann gerade nicht geprüft werden. Bitte kontrolliere den Zugang in der LEA-Integration.");return;}
    main.innerHTML=notice+`<div class="layout ${this._detailOpen?"details-open":""}"><div class="list"><div class="caption"><span>PERSÖNLICHE MELDUNGEN</span><span>${filtered.length} ${filtered.length===1?"Meldung":"Meldungen"}</span></div>${filtered.map(row=>`<button class="row ${leaEscape(row.meldungsart || "unknown")} ${row.meldungs_id===this._selected?"selected":""}" data-id="${leaEscape(row.meldungs_id)}"><div class="row-top"><span class="chip">${leaEscape(row.alarmstufe || LEA_LABELS[row.meldungsart] || "Meldung")}</span><time class="date">${leaEscape(leaTime(row.zeitstempel))}</time></div><h3>${leaEscape(row.meldebild || row.einsatzart || LEA_LABELS[row.meldungsart] || "Einsatzmeldung")}</h3><span class="place">${leaEscape(row.einsatzort || (account.include_details?"Kein Einsatzort übermittelt":"Einsatzdetails ausgeblendet"))}</span><div class="row-bottom"><span>${leaEscape(row.einsatznummer || "LEA")}</span><span class="arrow" aria-hidden="true">›</span></div></button>`).join("") || this._empty("Keine Treffer","Versuche einen anderen Suchbegriff.")}</div>${selected ? this._detail(selected,account) : ""}</div>`;
  }
  _empty(title,message) {return `<div class="empty"><div class="symbol">◇</div><h2>${leaEscape(title)}</h2><p>${leaEscape(message)}</p></div>`;}
  _sounds(account) {
    const audio=account.audio, sounds=(this._data?.sounds || []).filter(s=>/^[a-z0-9]+\.(mp3|m4a)$/.test(s.file || ""));
    if(!audio || !sounds.length) return this._empty("Alarmtöne benötigen Version 0.3.0","Bitte die Integration aktualisieren und Home Assistant neu starten.");
    const selected=sounds.find(s=>s.id===audio.sound);
    const players=(audio.players || []).map(id=>this._hass.states[id]?.attributes?.friendly_name || id);
    const settingsUrl=`/config/integrations/integration/lea_noe#config_entry=${encodeURIComponent(account.entry_id)}`;
    return `<section class="detail status-card"><h2>Alarmierung in Home Assistant</h2>${[["Automatische Wiedergabe",audio.enabled?"Aktiviert":"Deaktiviert"],["Auslöser","Neue LEA-Alarmierung"],["Gewählter Ton",selected?.label || audio.sound],["Lautstärke",`${audio.volume} %`],["Wiedergabegeräte",players.join(", ") || "Noch nicht ausgewählt"],["Dauer",audio.duration?`Höchstens ${audio.duration} Sekunden`:"Einmal vollständig"]].map(([k,v])=>`<div class="status-line"><span>${leaEscape(k)}</span><span>${leaEscape(v)}</span></div>`).join("")}<p class="privacy">Diese Einstellungen gelten nur für HA. Die automatische Wiedergabe funktioniert auch bei geschlossener HA-Ansicht. Beim ersten Einlesen werden vorhandene Meldungen nicht als neuer Alarm abgespielt.</p><p><a class="map-button" href="${settingsUrl}">Geräte und Ton in den LEA-Optionen einstellen</a></p><button class="map-button" data-audio-action="test_entity" ${audio.test_entity?"":"disabled"}>Ton auf HA-Geräten testen</button> <button class="map-button" data-audio-action="stop_entity" ${audio.stop_entity?"":"disabled"}>Wiedergabe stoppen</button><p class="privacy audio-result" role="status"></p><h2 style="margin-top:30px">Alle Originaltöne vorhören</h2><p class="privacy">Die Vorschau spielt auf diesem Browsergerät. Die Testtaste oben verwendet deine ausgewählten HA-Geräte.</p><div class="sound-list">${sounds.map(s=>`<div class="sound-item"><label>${leaEscape(s.label)} <small>· ${Math.round(s.seconds*10)/10} s</small></label><audio controls preload="none" aria-label="${leaEscape(s.label)} vorhören" src="/lea-noe-static/sounds/${s.file}"></audio></div>`).join("")}</div></section>`;
  }
  _detail(row,account) {
    return `<article class="detail ${leaEscape(row.meldungsart || "unknown")}"><button class="back" data-action="back">‹ Alle Meldungen</button><div class="kicker"><span class="chip">${leaEscape(row.alarmstufe || LEA_LABELS[row.meldungsart] || "Meldung")}</span><small>${leaEscape(LEA_LABELS[row.meldungsart] || "Meldung")}</small></div><h2>${leaEscape(row.meldebild || row.einsatzart || "Einsatzmeldung")}</h2><div class="meta">${[["Einsatznummer",row.einsatznummer || "Nicht übermittelt"],["Alarmiert am",leaTime(row.zeitstempel)],["Einsatzart",row.einsatzart || "Nicht übermittelt"],["Einsatzort",row.einsatzort || (account.include_details?"Nicht übermittelt":"Ausgeblendet")]].map(([key,value])=>`<div><label>${leaEscape(key)}</label><span>${leaEscape(value)}</span></div>`).join("")}</div>${account.include_details ? `<p class="message-body">${leaEscape(row.nachricht || "Kein zusätzlicher Meldungstext übermittelt.")}</p>` : `<p class="locked">Meldungstext und Einsatzort sind ausgeblendet. Du kannst die Anzeige in den <a href="/config/integrations/integration/lea_noe">Optionen der LEA-Integration</a> aktivieren.</p>`}<div class="detail-footer"><span aria-hidden="true">◉</span> Nur Anzeige · keine Rückmeldung an LEA</div></article>`;
  }
  _map(row,account) {
    const ready=leaCoordinates(row);
    return `<section class="detail status-card"><div class="kicker"><span class="chip">${leaEscape(row.alarmstufe || "LEA")}</span><small>${leaEscape(row.einsatznummer)}</small></div><h2>${leaEscape(row.einsatzort || "Einsatzkarte")}</h2>${ready ? `<div class="map-slot"></div>${this._mapConsentFor===row.meldungs_id?"":`<p class="privacy">Die Karte wird erst nach deinem Klick von OpenStreetMap geladen. Dabei werden der Kartenausschnitt und die Einsatzkoordinaten an OpenStreetMap übermittelt.</p><button class="map-button" data-action="load-map">OpenStreetMap-Karte laden</button>`}` : `<p class="locked">${account.include_details ? "Für diese Meldung wurden keine gültigen Koordinaten übermittelt." : "Einsatzkoordinaten sind ausgeblendet. Aktiviere bei Bedarf die Detailanzeige in den Optionen der Integration."}</p>`}</section>`;
  }
  _attachMap(row) {
    if(!leaCoordinates(row) || this._mapConsentFor!==row.meldungs_id) return;
    const slot=this.shadowRoot.querySelector(".map-slot");if(!slot)return;
    const lat=row.latitude,lon=row.longitude;
    const query=new URLSearchParams({bbox:`${Math.max(-180,lon-.012)},${Math.max(-90,lat-.008)},${Math.min(180,lon+.012)},${Math.min(90,lat+.008)}`,layer:"mapnik",marker:`${lat},${lon}`});
    const frame=document.createElement("iframe");frame.className="map";frame.title="Einsatzort auf OpenStreetMap";frame.referrerPolicy="no-referrer";frame.src=`https://www.openstreetmap.org/export/embed.html?${query}`;frame.loading="lazy";slot.append(frame);
  }
}

class LeaNoePanel extends HTMLElement {
  constructor(){super();this.attachShadow({mode:"open"});const card=document.createElement("lea-noe-card");card.setAttribute("panel","");card.setConfig({});this.shadowRoot.append(card);this._card=card;}
  set hass(hass){this._card.hass=hass;}
  set panel(panel){if(panel?.config)this._card.setConfig(panel.config);}
  set narrow(value){this._card.toggleAttribute("narrow",Boolean(value));}
}

if(!customElements.get("lea-noe-card")) customElements.define("lea-noe-card",LeaNoeCard);
if(!customElements.get("lea-noe-panel")) customElements.define("lea-noe-panel",LeaNoePanel);
window.customCards=window.customCards || [];
if(!window.customCards.some(card=>card.type==="lea-noe-card")) window.customCards.push({type:"lea-noe-card",name:"LEA BOS mobil",description:"Persönliche Meldungen im LEA-Design, ausschließlich lesend",preview:true});

