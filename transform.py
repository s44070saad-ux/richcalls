#!/usr/bin/env python3
"""Transform the partner-landing-page prototype into Rich Calls content/site.html.
Prototype is the spec: branding -> Rich Calls, real Supabase form submission,
extra Languages / Shift / Referral fields, absolute asset paths, mobile safety CSS,
and route-hash injection placeholders replaced at runtime by app/[[...path]]/route.ts.
"""
import pathlib, sys

src = pathlib.Path.home() / "workspace/ts-spaces/partner-landing-page/index.html"
out = pathlib.Path.home() / "workspace/richcalls-deploy/content/site.html"
html = src.read_text(encoding="utf-8")

def rep(old, new, count=1, required=True):
    global html
    if old not in html:
        if required:
            print(f"MISSING: {old[:90]!r}"); sys.exit(1)
        return
    html = html.replace(old, new, count)

# --- branding ---
html = html.replace("Partner Program", "Rich Calls")
html = html.replace("Pay-Per-Call Rich Calls", "Rich Calls — Pay-Per-Call Partner Network")
rep("<title>Rich Calls — Home Services First", "<title>Rich Calls — Home Services First")
# absolute asset paths (routes are nested: /trades/[slug])
html = html.replace('src="assets/', 'src="/assets/')

# --- config placeholders (route.ts replaces with env values at runtime) ---
rep("</head>", """<script>window.__RC__={url:"__SUPABASE_URL__",key:"__SUPABASE_ANON_KEY__"};</script>
<script>/* route initial view: __RC_INITIAL_VIEW__ */(function(){try{var v="__RC_VIEW__";var t="__RC_TRADE__";if(v==="home-services"&&!location.hash)location.hash="home-services";if(v==="trade"&&!location.hash)location.hash="trade-"+t;}catch(e){}})();</script>
<style id="rc-mobile">
/* Rich Calls mobile safety (Saad's release gate): no cropping, no oversized
   icons, no horizontal scroll on Android (~360px) or iOS (~390px). */
html,body{overflow-x:hidden;max-width:100%}
img,svg,video{max-width:100%}
h1,h2,h3,h4,p,li,a,span,b,td,th{overflow-wrap:break-word}
input,select,textarea{font-size:16px!important}
@media(max-width:640px){
  .sheet{margin:10px 8px;padding:52px 0 60px;border-radius:24px}
  .wrap,.wrap-narrow{padding-inline:16px}
  .hero h1{font-size:clamp(1.85rem,8.6vw,2.4rem);line-height:1.12}
  .sec-head h2{font-size:clamp(1.55rem,6.4vw,1.9rem);line-height:1.16}
  .hero .lede{font-size:1.02rem}
  .demo-frame{border-radius:14px}
  .demo-tabs button{min-height:44px}
  .mini-table{font-size:.78rem}
  .mini-table th,.mini-table td{padding:7px 8px}
  .route-viz,.demo-frame{overflow-x:auto;-webkit-overflow-scrolling:touch}
  .btn{white-space:normal;text-align:center;min-height:50px}
  .hero-ctas .btn{width:100%}
  .brand{font-size:.95rem}
  .check-row{gap:6px 14px;font-size:.85rem}
  .referral .big{font-size:1.55rem!important}
  .t-ic{width:40px!important;height:40px!important}
  .nav-panel{min-width:min(290px,calc(100vw - 32px))}
  table.mini-table{display:table;width:100%}
}
@media(max-width:480px){
  .foot-grid{grid-template-columns:1fr!important}
  .kpi-row{grid-template-columns:1fr 1fr}
}
</style>
</head>""")

# --- apply intro copy: real submission now ---
rep("The last question is a real buyer message. Answer it exactly as you would on Marketplace — it is the main thing we screen for. When your application is ready, you send it to the recruitment team on the channel where you found this page — that is how it reaches us.",
    "The last question is a real buyer message. Answer it exactly as you would on Marketplace — it is the main thing we screen for. Submitting sends your application straight to our recruitment team, and you will get a reference code to keep.")

# --- extra fields: Languages + Shift after Hours field block, Referral before About ---
hours_block_end = """              <p class="err" data-err-for="fHours">Please select your available hours.</p>
            </div>"""
rep(hours_block_end, hours_block_end + """
            <div class="field">
              <label for="fLanguages">Languages you speak <span class="req" aria-hidden="true">*</span></label>
              <input id="fLanguages" name="languages" type="text" placeholder="e.g. English, Hindi, Urdu" required />
              <p class="err" data-err-for="fLanguages">Please list the languages you speak.</p>
            </div>
            <div class="field">
              <label for="fShift">Shift you can cover <span class="req" aria-hidden="true">*</span></label>
              <select id="fShift" name="shift" required>
                <option value="">Select…</option>
                <option>UK hours</option><option>US hours</option><option>Both UK &amp; US hours</option><option>Flexible</option>
              </select>
              <p class="err" data-err-for="fShift">Please select the shift you can cover.</p>
            </div>""")

about_block_start = """            <div class="field full">
              <label for="fAbout">"""
rep(about_block_start, """            <div class="field full">
              <label for="fReferral">Referral code or who referred you <span style="color:var(--muted); font-weight:500;">(optional)</span></label>
              <input id="fReferral" name="referral" type="text" placeholder="e.g. partner name or referral code — leave blank if none" />
            </div>
""" + about_block_start)

# --- submit button + result copy ---
rep(">Prepare my application</button>", ">Submit my application</button>")
rep("<h3>Your application is ready</h3>", "<h3>Application received — thank you</h3>")
rep("Copy the application below and send it to the recruitment team on the channel where you found this page — our Facebook or Telegram partner group. Shortlisted applicants are contacted on WhatsApp for the next step.",
    "Your application has been sent to our recruitment team. Keep your reference code safe — shortlisted applicants are contacted on WhatsApp for the next step. You can also copy or download a copy of your application below for your own records.")
rep('<span class="copied-msg" id="copiedMsg" hidden>Copied — now send it to the team.</span>',
    '<span class="copied-msg" id="copiedMsg" hidden>Copied.</span>')

# --- form script: validators for new required fields ---
rep("    fExperience: function (v) { return v !== ''; },",
    "    fExperience: function (v) { return v !== ''; },\n    fLanguages: function (v) { return v.trim().length >= 2; },\n    fShift: function (v) { return v !== ''; },")

# --- form script: application text lines for new fields ---
rep("      'Campaign: ' + field('fCampaign').value,",
    """      'Campaign: ' + field('fCampaign').value,
      'Languages: ' + field('fLanguages').value.trim(),
      'Shift: ' + field('fShift').value,""")
rep("    var about = field('fAbout').value.trim();",
    """    var referral = field('fReferral').value.trim();
    if (referral) { lines.push('Referral: ' + referral); }
    var about = field('fAbout').value.trim();""")

# --- form script: real Supabase submission replacing local-only success ---
old_tail = """    currentText = lines.join('\\n');
    refCodeEl.textContent = ref;
    appTextEl.textContent = currentText;
    copiedMsg.hidden = true;
    form.style.display = 'none';
    result.classList.add('show');
    result.scrollIntoView({ behavior: 'smooth', block: 'start' });
    result.focus({ preventScroll: true });
  });"""
new_tail = """    currentText = lines.join('\\n');
    refCodeEl.textContent = ref;
    appTextEl.textContent = currentText;
    copiedMsg.hidden = true;
    var cfg = window.__RC__ || {};
    if (!cfg.url || !cfg.key || cfg.url.indexOf('__SUPABASE') === 0) {
      errorSummary.textContent = 'Applications are not open yet on this copy of the site — please try again shortly.';
      errorSummary.classList.add('show');
      return;
    }
    var payload = {
      full_name: field('fName').value.trim(),
      country: field('fCountry').value,
      city: field('fCity').value.trim(),
      whatsapp: field('fWhatsapp').value.trim(),
      email: field('fEmail').value.trim(),
      languages: field('fLanguages').value.trim(),
      english_level: field('fEnglish').value,
      device: field('fDevice').value,
      hours: field('fHours').value,
      shift_availability: field('fShift').value,
      experience: field('fExperience').value,
      campaign: field('fCampaign').value,
      screening_reply: field('fReply').value.trim(),
      referral: referral || null,
      about: about || null,
      reference_code: ref
    };
    var submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Sending…'; }
    fetch(cfg.url + '/rest/v1/partner_applications', {
      method: 'POST',
      headers: { 'apikey': cfg.key, 'Authorization': 'Bearer ' + cfg.key, 'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
      body: JSON.stringify(payload)
    }).then(function (r) {
      if (!r.ok) throw new Error('submit failed ' + r.status);
      form.style.display = 'none';
      result.classList.add('show');
      result.scrollIntoView({ behavior: 'smooth', block: 'start' });
      result.focus({ preventScroll: true });
    }).catch(function () {
      errorSummary.textContent = 'Your application could not be sent — please check your connection and try again. Your answers are still in the form.';
      errorSummary.classList.add('show');
      errorSummary.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }).finally(function () {
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Submit my application'; }
    });
  });"""
rep(old_tail, new_tail)

# stronger reference code: PP- + 6 uppercase alphanumerics
rep("var ref = 'PP-' + Date.now().toString(36).toUpperCase().slice(-6);",
    "var ref = 'PP-' + Array.from(crypto.getRandomValues(new Uint8Array(6))).map(function(b){return 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'[b%31];}).join('');")

out.write_text(html, encoding="utf-8")
print("OK", out, len(html))
