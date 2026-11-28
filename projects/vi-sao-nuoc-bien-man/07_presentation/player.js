/* Bộ dựng trình chiếu tất định — Tool 07 (videoProduction).
   Mỗi khung là hàm thuần của số khung: vp.seek(f) luôn cho cùng một hình, tua xuôi/ngược/nhảy cóc như nhau.
   Không dùng Date/Math.random/đồng hồ thật khi dựng. ?render=1: chế độ cho Tool 08 chụp khung. */
(function () {
  'use strict';
  const D = window.VP_DATA, SVG = window.VP_SVG || {}, NS = 'http://www.w3.org/2000/svg';
  const W = D.canvas.width, H = D.canvas.height, FPS = D.canvas.fps, TOTAL = D.total_frames;
  const RENDER = new URLSearchParams(location.search).has('render');
  const errors = [];
  window.addEventListener('error', e => errors.push(String(e.message || e)));

  // ---------- easing ----------
  const c1 = 1.70158, c3 = c1 + 1;
  const EASE = {
    linear: x => x, steps: x => x, linear_seamless: x => x,
    ease_in: x => x * x * x, ease_out: x => 1 - Math.pow(1 - x, 3),
    ease_in_out: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
    sine_in_out: x => .5 - .5 * Math.cos(Math.PI * x),
    back_out: x => 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2),
    back_in: x => c3 * x * x * x - c1 * x * x,
    elastic_out: x => x === 0 ? 0 : x === 1 ? 1 : Math.pow(2, -10 * x) * Math.sin((x * 10 - .75) * (2 * Math.PI) / 3) + 1,
    bounce_out: x => { const n = 7.5625, d = 2.75; if (x < 1 / d) return n * x * x; if (x < 2 / d) return n * (x -= 1.5 / d) * x + .75;
      if (x < 2.5 / d) return n * (x -= 2.25 / d) * x + .9375; return n * (x -= 2.625 / d) * x + .984375; },
  };
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const ease = (name, x) => (EASE[name] || EASE.ease_out)(clamp(x, 0, 1));
  const wave = (t, per) => Math.sin(2 * Math.PI * t / per);
  const hexA = (hex, a) => { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`; };

  // ---------- sân khấu ----------
  const stage = document.createElement('div');
  stage.id = 'stage';
  stage.style.width = W + 'px'; stage.style.height = H + 'px';
  document.body.appendChild(stage);
  if (RENDER) document.body.classList.add('render');

  let uid = 0;
  function instSVG(src) {
    // tiền tố id cho từng bản sao (nhiều khung dùng cùng một cảnh), giữ tên lớp ở data-layer
    const p = 'i' + (++uid) + '-';
    return src.replace(/\sid="([^"]+)"/g, (m, id) => ` id="${p}${id}" data-layer="${id}"`)
              .replace(/url\(#([^)]+)\)/g, (m, id) => `url(#${p}${id})`)
              .replace(/href="#([^"]+)"/g, (m, id) => `href="#${p}${id}"`);
  }

  function prepMotion(svg, motion) {
    const out = [];
    for (const m of motion || []) {
      const g = svg.querySelector(`[data-layer="${m.layer}"]`);
      if (!g) { errors.push(`thiếu lớp ${m.layer}`); continue; }
      const it = { m, g };
      if (m.recipe === 'rise' || m.recipe === 'fall') {
        // nhân đôi nội dung, lệch đúng một chu kỳ quãng đường -> trôi liền mạch không giật
        const inner = g.innerHTML;
        const dx = m.dx || 0, dy = m.dy || (m.recipe === 'fall' ? 540 : -360);
        g.innerHTML = `<g>${inner}</g><g transform="translate(${-dx} ${-dy})">${inner}</g>`;
        it.dx = dx; it.dy = dy;
      }
      if (m.recipe === 'along') {
        // hạt chạy dọc đường: lấy mẫu đường (mỗi ~2px) ngay lúc còn vẽ được, rồi ẩn hình tĩnh, sinh hạt mỗi khung
        let src = [];
        if (m.path) src = [...g.querySelectorAll('path[data-flow]')];
        else if (m.paths_from) { const o = svg.querySelector(`[data-layer="${m.paths_from}"]`); src = o ? [...o.querySelectorAll('path')] : []; }
        else if (m.paths) src = m.paths.map(d => { const q = document.createElementNS(NS, 'path'); q.setAttribute('d', d);
          q.setAttribute('fill', 'none'); q.setAttribute('stroke', 'none'); g.appendChild(q); return q; });
        if (!src.length) { errors.push(`along: lớp ${m.layer} không có đường`); continue; }
        it.tracks = src.map(q => {
          const len = q.getTotalLength(), n = Math.max(2, Math.ceil(len / 2)), pts = [];
          for (let i = 0; i <= n; i++) { const P = q.getPointAtLength(len * i / n); pts.push([P.x, P.y]); }
          const sizes = (q.getAttribute('data-flow') || '').split(/\s+/).filter(Boolean).map(Number);
          return { len, pts, sizes };
        });
        for (const c of [...g.children]) c.style.display = 'none';
        it.box = document.createElementNS(NS, 'g'); g.appendChild(it.box);
      }
      if (m.recipe === 'rotate' && !m.center) {
        let b; try { b = g.getBBox(); } catch { b = { x: 0, y: 0, width: 0, height: 0 }; } it.cx = b.x + b.width / 2; it.cy = b.y + b.height / 2;
      }
      out.push(it);
    }
    return out;
  }

  function applyMotion(list, t) {
    for (const it of list) {
      const m = it.m, per = m.period_s || 2;
      switch (m.recipe) {
        case 'bob': it.g.setAttribute('transform', `translate(${(m.ax || 0) * wave(t, per)} ${(m.amp || 6) * wave(t, per)})`); break;
        case 'rotate': { const [cx, cy] = m.center || [it.cx, it.cy]; it.g.setAttribute('transform', `rotate(${(360 * t / per) % 360} ${cx} ${cy})`); break; }
        case 'twinkle': case 'pulse_opacity': { const lo = m.lo ?? .35, hi = m.hi ?? 1; it.g.style.opacity = lo + (hi - lo) * (.5 + .5 * wave(t, per)); break; }
        case 'dashflow': it.g.querySelectorAll('path,line,polyline').forEach(p => p.style.strokeDashoffset = String(-(m.speed || 40) * t)); break;
        case 'rise': case 'fall': { const u = (t / per) % 1; it.g.setAttribute('transform', `translate(${it.dx * u} ${it.dy * u})`); break; }
        case 'along': it.box.innerHTML = alongFrame(it, t); break;
        default: errors.push('công thức lạ ' + m.recipe);
      }
    }
  }

  const lerpArr = (a, u) => { if (a.length < 2) return a[0] || 0; const x = clamp(u, 0, 1) * (a.length - 1), i = Math.min(a.length - 2, Math.floor(x));
    return a[i] + (a[i + 1] - a[i]) * (x - i); };
  function alongFrame(it, t) {
    const m = it.m, per = m.period_s || 1, col = m.color || '#FFFFFF', alpha = m.opacity ?? 1, fade = m.fade ?? 0.5;
    let out = '';
    it.tracks.forEach((tr, k) => {
      const gap = m.spacing ? +m.spacing : tr.len / (m.count || 1), n = m.spacing ? Math.ceil(tr.len / gap) + 1 : (m.count || 1);
      const ph = ((t / per + k * (m.stagger || 0)) % 1 + 1) % 1;
      for (let j = 0; j < n; j++) {
        const sArc = (ph + j) * gap; if (sArc > tr.len) continue;
        const u = sArc / tr.len, f = u * (tr.pts.length - 1), i = Math.min(tr.pts.length - 2, Math.floor(f)), r = f - i;
        const x = tr.pts[i][0] + (tr.pts[i + 1][0] - tr.pts[i][0]) * r, y = tr.pts[i][1] + (tr.pts[i + 1][1] - tr.pts[i][1]) * r;
        const op = alpha * clamp(Math.min(sArc, tr.len - sArc) / (fade * gap || 1), 0, 1);
        if (op <= 0.004) continue;
        if (m.shape === 'ripple') {
          const L = tr.sizes.length ? lerpArr(tr.sizes, u) : (m.size || 10);
          out += `<path d="M${(x - L).toFixed(1)} ${y.toFixed(1)} q${(L / 2).toFixed(1)} ${(-L * .22).toFixed(1)} ${L.toFixed(1)} 0 t${L.toFixed(1)} 0" stroke="${col}" stroke-opacity="${op.toFixed(3)}" stroke-width="${m.width || 3}" fill="none" stroke-linecap="round"/>`;
        } else out += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${m.r || 6}" fill="${col}" fill-opacity="${op.toFixed(3)}"/>`;
      }
    });
    return out;
  }

  function buildShot(i) {
    const s = D.shots[i];
    const root = document.createElement('div'); root.className = 'shot'; root.style.background = s.background;
    const cam = document.createElement('div'); cam.className = 'cam'; root.appendChild(cam);
    const over = document.createElement('div'); over.className = 'overlay'; root.appendChild(over);
    root.style.visibility = 'hidden'; stage.appendChild(root);   // phải nằm trong DOM thì mới đo được getBBox/getTotalLength
    const hasScene = s.elements.some(e => e.kind === 'scene');
    const plate = D.text_plate && (D.text_plate.always || hasScene) ? D.text_plate : null;
    const els = s.elements.map(e => {
      const n = document.createElement('div'); n.className = 'el';
      Object.assign(n.style, { left: e.box.x + '%', top: e.box.y + '%', width: e.box.w + '%', height: e.box.h + '%', zIndex: e.z });
      const it = { e, n, motion: [], draw: null };
      if (e.text !== undefined) {
        n.classList.add('txt', 'st-' + e.style);
        const sp = document.createElement('span'); sp.className = 'tx';
        sp.style.fontSize = e.font_px + 'px'; sp.style.color = e.color;
        sp.style.fontFamily = `'${(e.style === 'title' ? D.fonts.title : D.fonts.body) || 'Be Vietnam Pro'}', sans-serif`;
        if (plate) sp.style.background = hexA(plate.color, plate.opacity);
        sp.textContent = e.text; n.appendChild(sp); it.span = sp; over.appendChild(n);
      } else if (SVG[e.asset]) {
        n.innerHTML = instSVG(SVG[e.asset]);
        const svg = n.querySelector('svg'); svg.setAttribute('width', '100%'); svg.setAttribute('height', '100%');
        cam.appendChild(n);
        it.motion = prepMotion(svg, (D.assets[e.asset] || {}).motion);
        if (e.enter && e.enter.anim === 'draw') {
          it.draw = [...svg.querySelectorAll('path,line,polyline,circle,ellipse,rect')].map(p => {
            let L = 0; try { L = p.getTotalLength(); } catch { return null; }   // phần tử trong <defs> không vẽ
            p.style.strokeDasharray = L; return [p, L]; }).filter(Boolean);
        }
      } else {
        const img = document.createElement('img'); img.src = (D.assets[e.asset] || {}).file || ''; img.alt = e.asset;
        n.appendChild(img); cam.appendChild(n);
      }
      return it;
    });
    return { s, root, cam, over, els };
  }
  const shots = D.shots.map((_, i) => buildShot(i));
  shots.forEach(sh => { stage.removeChild(sh.root); sh.root.style.visibility = ''; });

  function elementState(it, f) {
    const e = it.e, b = e.box, bx = b.x / 100 * W, by = b.y / 100 * H, bw = b.w / 100 * W, bh = b.h / 100 * H;
    let op = 1, tx = 0, ty = 0, sx = 1, sy = 1, rot = 0, origin = '50% 50%', clip = '', chars = null, drawP = 1;
    if (e.enter) {
      const en = e.enter;
      if (f < en.start) return null;
      const x = (f - en.start) / en.dur, p = ease(en.ease, x);
      switch (en.anim) {
        case 'fade': case 'morph': op *= p; break;
        case 'draw': drawP = clamp(x, 0, 1); op *= Math.min(1, x * 3); break;
        case 'pop': case 'scale_in': sx *= p; sy *= p; break;
        case 'grow': sy *= p; origin = '50% 100%'; break;
        case 'drop': {
          ty -= (by + bh) * (1 - p);
          const k = (f - (en.start + en.dur)) / 4;            // bẹp rồi bật lại khi chạm (4 khung)
          if (k >= 0 && k < 1) { const s_ = Math.sin(Math.PI * k) * .15; sx *= 1 + s_; sy *= 1 - s_; origin = '50% 100%'; }
          break; }
        case 'slide_up': ty += H * .15 * (1 - p); op *= Math.min(1, x * 3); break;
        case 'slide_down': ty -= (by + bh) * (1 - p); break;
        case 'slide_left': tx += (W - bx) * (1 - p); break;
        case 'slide_right': tx -= (bx + bw) * (1 - p); break;
        case 'wipe': clip = `inset(0 ${(1 - p) * 100}% 0 0)`; break;
        case 'typewriter': chars = Math.floor(clamp(x, 0, 1) * (e.text || '').length); break;
        case 'none': break;
        default: errors.push('lượt vào lạ ' + en.anim);
      }
    }
    if (e.exit && f >= e.exit.start) {
      const ex = e.exit, x = (f - ex.start) / ex.dur, p = ease(ex.ease, x);
      if (x >= 1 && ex.anim !== 'none') return null;
      if (ex.anim === 'fade') op *= 1 - p;
      else if (ex.anim === 'scale_out') { sx *= Math.max(0, 1 - p); sy *= Math.max(0, 1 - p); }
      else if (ex.anim === 'slide_left') tx -= (bx + bw) * p;
      else if (ex.anim === 'slide_right') tx += (W - bx) * p;
      else errors.push('lượt ra lạ ' + ex.anim);
    }
    if (e.loop && !e.layer_motion && e.kind === 'scene') {
      // cảnh cả khung không được trôi/đập cả khối: chuyển động phải khai ở lớp (assets.yaml → motion)
      if (!it.warned) { errors.push(`${e.asset}: vòng lặp '${e.loop.anim}' trên cảnh nhưng asset chưa khai motion`); it.warned = true; }
    } else if (e.loop && !e.layer_motion && f >= e.loop.start) {
      const t = (f - e.loop.start) / FPS, per = e.loop.period / FPS;
      switch (e.loop.anim) {
        case 'bob': ty += 8 * wave(t, per); break;
        case 'pulse': if (e.kind === 'diagram') op *= .3 + .7 * (.5 + .5 * wave(t, per)); else { const k = 1 + .045 * wave(t, per); sx *= k; sy *= k; } break;
        case 'rotate': rot += (360 * t / per) % 360; break;
        case 'wiggle': rot += 7 * wave(t, per); break;
        case 'shimmer': op *= .78 + .22 * (.5 + .5 * wave(t, per)); break;
        case 'blink_slow': op *= .4 + .6 * (.5 + .5 * Math.cos(2 * Math.PI * t / per)); break;
        case 'flow': { const u = (t / per) % 1; ty += u * bh * .9; op *= Math.min(1, (1 - u) / .25); break; }
        default: errors.push('vòng lặp lạ ' + e.loop.anim);
      }
    }
    return { op, tx, ty, sx, sy, rot, origin, clip, chars, drawP };
  }

  function cameraTransform(s, f) {
    const c = s.camera || {}, a = +c.amount || 0, prog = ease('ease_in_out', (f - s.start) / Math.max(1, s.end - s.start));
    let k = 1, tx = 0, ty = 0;
    switch (c.move) {
      case 'zoom_in': k = 1 + a * prog; break;
      case 'zoom_out': k = 1 + a * (1 - prog); break;
      case 'pan_right': k = 1 + a; tx = -a * W * (prog - .5); break;
      case 'pan_left': k = 1 + a; tx = a * W * (prog - .5); break;
      case 'pan_down': k = 1 + a; ty = -a * H * (prog - .5); break;
      case 'pan_up': k = 1 + a; ty = a * H * (prog - .5); break;
    }
    return `translate(${tx}px,${ty}px) scale(${k})`;
  }

  function renderShot(sh, f) {
    const s = sh.s;
    sh.cam.style.transform = cameraTransform(s, f);
    const t = (f - s.start) / FPS;
    for (const it of sh.els) {
      const st = elementState(it, f);
      if (!st) { it.n.style.visibility = 'hidden'; continue; }
      const n = it.n;
      n.style.visibility = st.op > 0.001 ? 'visible' : 'hidden';
      n.style.opacity = st.op;
      n.style.transformOrigin = st.origin;
      n.style.transform = `translate(${st.tx}px,${st.ty}px) rotate(${st.rot}deg) scale(${st.sx},${st.sy})`;
      n.style.clipPath = st.clip;
      if (it.span) it.span.textContent = st.chars === null ? it.e.text : it.e.text.slice(0, st.chars);
      if (it.draw) for (const [p, L] of it.draw) p.style.strokeDashoffset = L * (1 - st.drawP);
      if (it.motion.length) applyMotion(it.motion, t);
    }
  }

  function shotIndexAt(f) {
    for (let i = D.shots.length - 1; i >= 0; i--) if (f >= D.shots[i].start) return i;
    return 0;
  }

  let current = -1, curShot = null, inTransition = false;
  function seekSync(f) {
    f = clamp(Math.round(f), 0, TOTAL - 1);
    const i = shotIndexAt(f), sh = shots[i], s = sh.s;
    const tr = s.transition || { type: 'cut', frames: 0 };
    const inTr = i > 0 && tr.frames > 0 && f - s.start < tr.frames;
    const want = inTr ? [shots[i - 1], sh] : [sh];
    // tháo hết rồi gắn lại: buộc Chrome vẽ mới toàn bộ, không dùng lại phần đã vẽ của khung trước (tất định theo lịch sử tua)
    for (const c of [...stage.children]) stage.removeChild(c);
    want.forEach(w => stage.appendChild(w.root));
    for (const w of want) { w.root.style.opacity = 1; w.root.style.transform = ''; }
    if (inTr) {
      const prev = shots[i - 1], p = ease('ease_in_out', (f - s.start) / tr.frames);
      stage.appendChild(sh.root);  // khung mới luôn nằm trên
      renderShot(prev, f);
      switch (tr.type) {
        case 'crossfade': sh.root.style.opacity = p; break;
        case 'push_up': prev.root.style.transform = `translateY(${-p * H}px)`; sh.root.style.transform = `translateY(${(1 - p) * H}px)`; break;
        case 'push_down': prev.root.style.transform = `translateY(${p * H}px)`; sh.root.style.transform = `translateY(${-(1 - p) * H}px)`; break;
        case 'push_left': prev.root.style.transform = `translateX(${-p * W}px)`; sh.root.style.transform = `translateX(${(1 - p) * W}px)`; break;
        case 'push_right': prev.root.style.transform = `translateX(${p * W}px)`; sh.root.style.transform = `translateX(${-(1 - p) * W}px)`; break;
        case 'zoom_through': prev.root.style.transform = `scale(${1 + .5 * p})`; prev.root.style.opacity = 1 - p;
          sh.root.style.opacity = p; sh.root.style.transform = `scale(${.92 + .08 * p})`; break;
      }
    }
    renderShot(sh, f);
    current = f; curShot = sh; inTransition = inTr;
    return { frame: f, shot: s.id };
  }

  // sẵn sàng: font nạp xong + ảnh nạp xong
  const imgs = [...stage.ownerDocument.querySelectorAll('img')];
  shots.forEach(sh => sh.root.querySelectorAll('img').forEach(im => imgs.push(im)));
  const ready = Promise.all([document.fonts ? document.fonts.ready : Promise.resolve(),
    ...imgs.map(im => im.complete ? Promise.resolve() : new Promise(r => { im.onload = r; im.onerror = () => { errors.push('lỗi ảnh ' + im.src); r(); }; }))]);

  function measure() {
    // chữ tràn hộp / ra ngoài vùng an toàn (đo trên DOM ở khung hiện tại)
    const out = [], sr = stage.getBoundingClientRect(), k = sr.width / W, m = D.safe_area * W, mh = D.safe_area * H;
    if (inTransition || !curShot) return out;          // đang chuyển cảnh: khung cũ bị phóng/đẩy có chủ ý
    { const sh = curShot;
      for (const it of sh.els) {
        if (!it.span || it.n.style.visibility === 'hidden') continue;
        const r = it.span.getBoundingClientRect(), b = it.n.getBoundingClientRect(), tol = 2 * k;
        if (r.width > b.width + tol || r.height > b.height + tol) out.push(`${sh.s.id}/${it.e.id}: chữ tràn hộp (${Math.round(r.width / k)}×${Math.round(r.height / k)} > ${Math.round(b.width / k)}×${Math.round(b.height / k)})`);
        const L = (r.left - sr.left) / k, T = (r.top - sr.top) / k, R = (r.right - sr.left) / k, B = (r.bottom - sr.top) / k;
        if (L < m - 1 || T < mh - 1 || R > W - m + 1 || B > H - mh + 1) out.push(`${sh.s.id}/${it.e.id}: chữ ra ngoài vùng an toàn 5%`);
      }
    }
    return out;
  }

  window.vp = {
    total: TOTAL, fps: FPS, width: W, height: H, errors, ready,
    seek: f => ready.then(() => seekSync(f)),
    measure, shotAt: f => D.shots[shotIndexAt(f)].id,
  };

  // ---------- chế độ xem (không dùng khi dựng) ----------
  ready.then(() => seekSync(0));
  if (RENDER) return;
  const ui = document.getElementById('ui');
  if (!ui) return;
  const audio = document.getElementById('voice'), play = document.getElementById('play'), bar = document.getElementById('bar'),
        lab = document.getElementById('lab'), safe = document.getElementById('safe');
  bar.max = TOTAL - 1;
  const fit = () => { const k = Math.min(innerWidth / W, (innerHeight - ui.offsetHeight) / H); stage.style.transform = `scale(${k})`;
    stage.parentElement && (document.body.style.setProperty('--k', k)); };
  addEventListener('resize', fit); fit();
  const show = f => { seekSync(f); bar.value = f; lab.textContent = `khung ${f}/${TOTAL - 1} · ${(f / FPS).toFixed(2)}s · ${D.shots[shotIndexAt(f)].id}`; };
  let raf = 0;
  const loop = () => { show(Math.floor(audio.currentTime * FPS)); if (!audio.paused && !audio.ended) raf = requestAnimationFrame(loop); else play.textContent = '▶ Phát'; };
  play.onclick = () => { if (audio.paused) { if (audio.ended || current >= TOTAL - 1) audio.currentTime = 0; audio.play(); play.textContent = '❚❚ Dừng'; loop(); } else audio.pause(); };
  bar.oninput = () => { audio.currentTime = bar.value / FPS; show(+bar.value); };
  safe.onchange = () => stage.classList.toggle('show-safe', safe.checked);
  addEventListener('keydown', e => { if (e.key === ' ') { e.preventDefault(); play.onclick(); }
    if (e.key === 'ArrowRight') { audio.currentTime = Math.min(TOTAL - 1, current + 1) / FPS; show(current + 1); }
    if (e.key === 'ArrowLeft') { audio.currentTime = Math.max(0, current - 1) / FPS; show(current - 1); } });
  ready.then(() => show(0));
})();
