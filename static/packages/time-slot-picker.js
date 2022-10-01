this.IronWeb = this.IronWeb || {};
this.IronWeb.TimeSlotPicker = (function () {
  'use strict';

  function _defineProperty(obj, key, value) {
    if (key in obj) {
      Object.defineProperty(obj, key, {
        value: value,
        enumerable: true,
        configurable: true,
        writable: true
      });
    } else {
      obj[key] = value;
    }

    return obj;
  }

  function _extends() {
    _extends = Object.assign || function (target) {
      for (var i = 1; i < arguments.length; i++) {
        var source = arguments[i];

        for (var key in source) {
          if (Object.prototype.hasOwnProperty.call(source, key)) {
            target[key] = source[key];
          }
        }
      }

      return target;
    };

    return _extends.apply(this, arguments);
  }

  function ownKeys(object, enumerableOnly) {
    var keys = Object.keys(object);

    if (Object.getOwnPropertySymbols) {
      var symbols = Object.getOwnPropertySymbols(object);
      if (enumerableOnly) symbols = symbols.filter(function (sym) {
        return Object.getOwnPropertyDescriptor(object, sym).enumerable;
      });
      keys.push.apply(keys, symbols);
    }

    return keys;
  }

  function _objectSpread2(target) {
    for (var i = 1; i < arguments.length; i++) {
      var source = arguments[i] != null ? arguments[i] : {};

      if (i % 2) {
        ownKeys(Object(source), true).forEach(function (key) {
          _defineProperty(target, key, source[key]);
        });
      } else if (Object.getOwnPropertyDescriptors) {
        Object.defineProperties(target, Object.getOwnPropertyDescriptors(source));
      } else {
        ownKeys(Object(source)).forEach(function (key) {
          Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key));
        });
      }
    }

    return target;
  }

  function _objectWithoutPropertiesLoose(source, excluded) {
    if (source == null) return {};
    var target = {};
    var sourceKeys = Object.keys(source);
    var key, i;

    for (i = 0; i < sourceKeys.length; i++) {
      key = sourceKeys[i];
      if (excluded.indexOf(key) >= 0) continue;
      target[key] = source[key];
    }

    return target;
  }

  function _objectWithoutProperties(source, excluded) {
    if (source == null) return {};

    var target = _objectWithoutPropertiesLoose(source, excluded);

    var key, i;

    if (Object.getOwnPropertySymbols) {
      var sourceSymbolKeys = Object.getOwnPropertySymbols(source);

      for (i = 0; i < sourceSymbolKeys.length; i++) {
        key = sourceSymbolKeys[i];
        if (excluded.indexOf(key) >= 0) continue;
        if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue;
        target[key] = source[key];
      }
    }

    return target;
  }

  function _slicedToArray(arr, i) {
    return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _nonIterableRest();
  }

  function _arrayWithHoles(arr) {
    if (Array.isArray(arr)) return arr;
  }

  function _iterableToArrayLimit(arr, i) {
    if (!(Symbol.iterator in Object(arr) || Object.prototype.toString.call(arr) === "[object Arguments]")) {
      return;
    }

    var _arr = [];
    var _n = true;
    var _d = false;
    var _e = undefined;

    try {
      for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) {
        _arr.push(_s.value);

        if (i && _arr.length === i) break;
      }
    } catch (err) {
      _d = true;
      _e = err;
    } finally {
      try {
        if (!_n && _i["return"] != null) _i["return"]();
      } finally {
        if (_d) throw _e;
      }
    }

    return _arr;
  }

  function _nonIterableRest() {
    throw new TypeError("Invalid attempt to destructure non-iterable instance");
  }

  var n,
      u,
      i,
      t,
      o,
      r,
      f = {},
      e = [],
      c = /acit|ex(?:s|g|n|p|$)|rph|grid|ows|mnc|ntw|ine[ch]|zoo|^ord/i;

  function s(n, l) {
    for (var u in l) n[u] = l[u];

    return n;
  }

  function a(n) {
    var l = n.parentNode;
    l && l.removeChild(n);
  }

  function v(n, l, u) {
    var i,
        t = arguments,
        o = {};

    for (i in l) "key" !== i && "ref" !== i && (o[i] = l[i]);

    if (arguments.length > 3) for (u = [u], i = 3; i < arguments.length; i++) u.push(t[i]);
    if (null != u && (o.children = u), "function" == typeof n && null != n.defaultProps) for (i in n.defaultProps) void 0 === o[i] && (o[i] = n.defaultProps[i]);
    return h(n, o, l && l.key, l && l.ref);
  }

  function h(l, u, i, t) {
    var o = {
      type: l,
      props: u,
      key: i,
      ref: t,
      __k: null,
      __: null,
      __b: 0,
      __e: null,
      __d: void 0,
      __c: null,
      constructor: void 0
    };
    return n.vnode && n.vnode(o), o;
  }

  function d(n) {
    return n.children;
  }

  function y(n, l) {
    this.props = n, this.context = l;
  }

  function m(n, l) {
    if (null == l) return n.__ ? m(n.__, n.__.__k.indexOf(n) + 1) : null;

    for (var u; l < n.__k.length; l++) if (null != (u = n.__k[l]) && null != u.__e) return u.__e;

    return "function" == typeof n.type ? m(n) : null;
  }

  function w(n) {
    var l, u;

    if (null != (n = n.__) && null != n.__c) {
      for (n.__e = n.__c.base = null, l = 0; l < n.__k.length; l++) if (null != (u = n.__k[l]) && null != u.__e) {
        n.__e = n.__c.base = u.__e;
        break;
      }

      return w(n);
    }
  }

  function g(l) {
    (!l.__d && (l.__d = !0) && 1 === u.push(l) || t !== n.debounceRendering) && ((t = n.debounceRendering) || i)(k);
  }

  function k() {
    var n, l, i, t, o, r, f;

    for (u.sort(function (n, l) {
      return l.__v.__b - n.__v.__b;
    }); n = u.pop();) n.__d && (i = void 0, t = void 0, r = (o = (l = n).__v).__e, (f = l.__P) && (i = [], t = z(f, o, s({}, o), l.__n, void 0 !== f.ownerSVGElement, null, i, null == r ? m(o) : r), A(i, o), t != r && w(o)));
  }

  function _(n, l, u, i, t, o, r, c, s) {
    var v,
        h,
        p,
        d,
        y,
        w,
        g,
        k = u && u.__k || e,
        _ = k.length;
    if (c == f && (c = null != o ? o[0] : _ ? m(u, 0) : null), v = 0, l.__k = b(l.__k, function (u) {
      if (null != u) {
        if (u.__ = l, u.__b = l.__b + 1, null === (p = k[v]) || p && u.key == p.key && u.type === p.type) k[v] = void 0;else for (h = 0; h < _; h++) {
          if ((p = k[h]) && u.key == p.key && u.type === p.type) {
            k[h] = void 0;
            break;
          }

          p = null;
        }

        if (d = z(n, u, p = p || f, i, t, o, r, c, s), (h = u.ref) && p.ref != h && (g || (g = []), p.ref && g.push(p.ref, null, u), g.push(h, u.__c || d, u)), null != d) {
          var e;
          if (null == w && (w = d), void 0 !== u.__d) e = u.__d, u.__d = void 0;else if (o == p || d != c || null == d.parentNode) {
            n: if (null == c || c.parentNode !== n) n.appendChild(d), e = null;else {
              for (y = c, h = 0; (y = y.nextSibling) && h < _; h += 2) if (y == d) break n;

              n.insertBefore(d, c), e = c;
            }

            "option" == l.type && (n.value = "");
          }
          c = void 0 !== e ? e : d.nextSibling, "function" == typeof l.type && (l.__d = c);
        } else c && p.__e == c && c.parentNode != n && (c = m(p));
      }

      return v++, u;
    }), l.__e = w, null != o && "function" != typeof l.type) for (v = o.length; v--;) null != o[v] && a(o[v]);

    for (v = _; v--;) null != k[v] && j(k[v], k[v]);

    if (g) for (v = 0; v < g.length; v++) $(g[v], g[++v], g[++v]);
  }

  function b(n, l, u) {
    if (null == u && (u = []), null == n || "boolean" == typeof n) l && u.push(l(null));else if (Array.isArray(n)) for (var i = 0; i < n.length; i++) b(n[i], l, u);else u.push(l ? l("string" == typeof n || "number" == typeof n ? h(null, n, null, null) : null != n.__e || null != n.__c ? h(n.type, n.props, n.key, null) : n) : n);
    return u;
  }

  function x(n, l, u, i, t) {
    var o;

    for (o in u) o in l || C(n, o, null, u[o], i);

    for (o in l) t && "function" != typeof l[o] || "value" === o || "checked" === o || u[o] === l[o] || C(n, o, l[o], u[o], i);
  }

  function P(n, l, u) {
    "-" === l[0] ? n.setProperty(l, u) : n[l] = "number" == typeof u && !1 === c.test(l) ? u + "px" : null == u ? "" : u;
  }

  function C(n, l, u, i, t) {
    var o, r, f, e, c;
    if (t ? "className" === l && (l = "class") : "class" === l && (l = "className"), "key" === l || "children" === l) ;else if ("style" === l) {
      if (o = n.style, "string" == typeof u) o.cssText = u;else {
        if ("string" == typeof i && (o.cssText = "", i = null), i) for (r in i) u && r in u || P(o, r, "");
        if (u) for (f in u) i && u[f] === i[f] || P(o, f, u[f]);
      }
    } else "o" === l[0] && "n" === l[1] ? (e = l !== (l = l.replace(/Capture$/, "")), c = l.toLowerCase(), l = (c in n ? c : l).slice(2), u ? (i || n.addEventListener(l, N, e), (n.l || (n.l = {}))[l] = u) : n.removeEventListener(l, N, e)) : "list" !== l && "tagName" !== l && "form" !== l && "type" !== l && "size" !== l && !t && l in n ? n[l] = null == u ? "" : u : "function" != typeof u && "dangerouslySetInnerHTML" !== l && (l !== (l = l.replace(/^xlink:?/, "")) ? null == u || !1 === u ? n.removeAttributeNS("http://www.w3.org/1999/xlink", l.toLowerCase()) : n.setAttributeNS("http://www.w3.org/1999/xlink", l.toLowerCase(), u) : null == u || !1 === u && !/^ar/.test(l) ? n.removeAttribute(l) : n.setAttribute(l, u));
  }

  function N(l) {
    this.l[l.type](n.event ? n.event(l) : l);
  }

  function z(l, u, i, t, o, r, f, e, c) {
    var a,
        v,
        h,
        p,
        m,
        w,
        g,
        k,
        b,
        x,
        P = u.type;
    if (void 0 !== u.constructor) return null;
    (a = n.__b) && a(u);

    try {
      n: if ("function" == typeof P) {
        if (k = u.props, b = (a = P.contextType) && t[a.__c], x = a ? b ? b.props.value : a.__ : t, i.__c ? g = (v = u.__c = i.__c).__ = v.__E : ("prototype" in P && P.prototype.render ? u.__c = v = new P(k, x) : (u.__c = v = new y(k, x), v.constructor = P, v.render = D), b && b.sub(v), v.props = k, v.state || (v.state = {}), v.context = x, v.__n = t, h = v.__d = !0, v.__h = []), null == v.__s && (v.__s = v.state), null != P.getDerivedStateFromProps && (v.__s == v.state && (v.__s = s({}, v.__s)), s(v.__s, P.getDerivedStateFromProps(k, v.__s))), p = v.props, m = v.state, h) null == P.getDerivedStateFromProps && null != v.componentWillMount && v.componentWillMount(), null != v.componentDidMount && v.__h.push(v.componentDidMount);else {
          if (null == P.getDerivedStateFromProps && k !== p && null != v.componentWillReceiveProps && v.componentWillReceiveProps(k, x), !v.__e && null != v.shouldComponentUpdate && !1 === v.shouldComponentUpdate(k, v.__s, x)) {
            for (v.props = k, v.state = v.__s, v.__d = !1, v.__v = u, u.__e = i.__e, u.__k = i.__k, v.__h.length && f.push(v), a = 0; a < u.__k.length; a++) u.__k[a] && (u.__k[a].__ = u);

            break n;
          }

          null != v.componentWillUpdate && v.componentWillUpdate(k, v.__s, x), null != v.componentDidUpdate && v.__h.push(function () {
            v.componentDidUpdate(p, m, w);
          });
        }
        v.context = x, v.props = k, v.state = v.__s, (a = n.__r) && a(u), v.__d = !1, v.__v = u, v.__P = l, a = v.render(v.props, v.state, v.context), u.__k = null != a && a.type == d && null == a.key ? a.props.children : Array.isArray(a) ? a : [a], null != v.getChildContext && (t = s(s({}, t), v.getChildContext())), h || null == v.getSnapshotBeforeUpdate || (w = v.getSnapshotBeforeUpdate(p, m)), _(l, u, i, t, o, r, f, e, c), v.base = u.__e, v.__h.length && f.push(v), g && (v.__E = v.__ = null), v.__e = !1;
      } else u.__e = T(i.__e, u, i, t, o, r, f, c);

      (a = n.diffed) && a(u);
    } catch (l) {
      n.__e(l, u, i);
    }

    return u.__e;
  }

  function A(l, u) {
    n.__c && n.__c(u, l), l.some(function (u) {
      try {
        l = u.__h, u.__h = [], l.some(function (n) {
          n.call(u);
        });
      } catch (l) {
        n.__e(l, u.__v);
      }
    });
  }

  function T(n, l, u, i, t, o, r, c) {
    var s,
        a,
        v,
        h,
        p,
        d = u.props,
        y = l.props;
    if (t = "svg" === l.type || t, null != o) for (s = 0; s < o.length; s++) if (null != (a = o[s]) && ((null === l.type ? 3 === a.nodeType : a.localName === l.type) || n == a)) {
      n = a, o[s] = null;
      break;
    }

    if (null == n) {
      if (null === l.type) return document.createTextNode(y);
      n = t ? document.createElementNS("http://www.w3.org/2000/svg", l.type) : document.createElement(l.type, y.is && {
        is: y.is
      }), o = null;
    }

    if (null === l.type) d !== y && n.data != y && (n.data = y);else if (l !== u) {
      if (null != o && (o = e.slice.call(n.childNodes)), v = (d = u.props || f).dangerouslySetInnerHTML, h = y.dangerouslySetInnerHTML, !c) {
        if (d === f) for (d = {}, p = 0; p < n.attributes.length; p++) d[n.attributes[p].name] = n.attributes[p].value;
        (h || v) && (h && v && h.__html == v.__html || (n.innerHTML = h && h.__html || ""));
      }

      x(n, y, d, t, c), l.__k = l.props.children, h || _(n, l, u, i, "foreignObject" !== l.type && t, o, r, f, c), c || ("value" in y && void 0 !== y.value && y.value !== n.value && (n.value = null == y.value ? "" : y.value), "checked" in y && void 0 !== y.checked && y.checked !== n.checked && (n.checked = y.checked));
    }
    return n;
  }

  function $(l, u, i) {
    try {
      "function" == typeof l ? l(u) : l.current = u;
    } catch (l) {
      n.__e(l, i);
    }
  }

  function j(l, u, i) {
    var t, o, r;

    if (n.unmount && n.unmount(l), (t = l.ref) && (t.current && t.current !== l.__e || $(t, null, u)), i || "function" == typeof l.type || (i = null != (o = l.__e)), l.__e = l.__d = void 0, null != (t = l.__c)) {
      if (t.componentWillUnmount) try {
        t.componentWillUnmount();
      } catch (l) {
        n.__e(l, u);
      }
      t.base = t.__P = null;
    }

    if (t = l.__k) for (r = 0; r < t.length; r++) t[r] && j(t[r], u, i);
    null != o && a(o);
  }

  function D(n, l, u) {
    return this.constructor(n, u);
  }

  function E(l, u, i) {
    var t, r, c;
    n.__ && n.__(l, u), r = (t = i === o) ? null : i && i.__k || u.__k, l = v(d, null, [l]), c = [], z(u, (t ? u : i || u).__k = l, r || f, f, void 0 !== u.ownerSVGElement, i && !t ? [i] : r ? null : e.slice.call(u.childNodes), c, i || f, t), A(c, l);
  }

  n = {
    __e: function (n, l) {
      for (var u, i; l = l.__;) if ((u = l.__c) && !u.__) try {
        if (u.constructor && null != u.constructor.getDerivedStateFromError && (i = !0, u.setState(u.constructor.getDerivedStateFromError(n))), null != u.componentDidCatch && (i = !0, u.componentDidCatch(n)), i) return g(u.__E = u);
      } catch (l) {
        n = l;
      }

      throw n;
    }
  }, y.prototype.setState = function (n, l) {
    var u;
    u = this.__s !== this.state ? this.__s : this.__s = s({}, this.state), "function" == typeof n && (n = n(u, this.props)), n && s(u, n), null != n && this.__v && (l && this.__h.push(l), g(this));
  }, y.prototype.forceUpdate = function (n) {
    this.__v && (this.__e = !0, n && this.__h.push(n), g(this));
  }, y.prototype.render = d, u = [], i = "function" == typeof Promise ? Promise.prototype.then.bind(Promise.resolve()) : setTimeout, o = f, r = 0;

  var t$1,
      r$1,
      u$1,
      i$1 = [],
      o$1 = n.__r,
      f$1 = n.diffed,
      c$1 = n.__c,
      e$1 = n.unmount;

  function a$1(t) {
    n.__h && n.__h(r$1);
    var u = r$1.__H || (r$1.__H = {
      __: [],
      __h: []
    });
    return t >= u.__.length && u.__.push({}), u.__[t];
  }

  function v$1(n) {
    return m$1(x$1, n);
  }

  function m$1(n, u, i) {
    var o = a$1(t$1++);
    return o.__c || (o.__c = r$1, o.__ = [i ? i(u) : x$1(void 0, u), function (t) {
      var r = n(o.__[0], t);
      o.__[0] !== r && (o.__[0] = r, o.__c.setState({}));
    }]), o.__;
  }

  function p(n, u) {
    var i = a$1(t$1++);
    q(i.__H, u) && (i.__ = n, i.__H = u, r$1.__H.__h.push(i));
  }

  function l(n, u) {
    var i = a$1(t$1++);
    q(i.__H, u) && (i.__ = n, i.__H = u, r$1.__h.push(i));
  }

  function y$1(n) {
    return s$1(function () {
      return {
        current: n
      };
    }, []);
  }

  function s$1(n, r) {
    var u = a$1(t$1++);
    return q(u.__H, r) ? (u.__H = r, u.__h = n, u.__ = n()) : u.__;
  }

  function F() {
    i$1.some(function (t) {
      if (t.__P) try {
        t.__H.__h.forEach(_$1), t.__H.__h.forEach(g$1), t.__H.__h = [];
      } catch (r) {
        return n.__e(r, t.__v), !0;
      }
    }), i$1 = [];
  }

  function _$1(n) {
    n.t && n.t();
  }

  function g$1(n) {
    var t = n.__();

    "function" == typeof t && (n.t = t);
  }

  function q(n, t) {
    return !n || t.some(function (t, r) {
      return t !== n[r];
    });
  }

  function x$1(n, t) {
    return "function" == typeof t ? t(n) : t;
  }

  n.__r = function (n) {
    o$1 && o$1(n), t$1 = 0, (r$1 = n.__c).__H && (r$1.__H.__h.forEach(_$1), r$1.__H.__h.forEach(g$1), r$1.__H.__h = []);
  }, n.diffed = function (t) {
    f$1 && f$1(t);
    var r = t.__c;

    if (r) {
      var o = r.__H;
      o && o.__h.length && (1 !== i$1.push(r) && u$1 === n.requestAnimationFrame || ((u$1 = n.requestAnimationFrame) || function (n) {
        var t,
            r = function () {
          clearTimeout(u), cancelAnimationFrame(t), setTimeout(n);
        },
            u = setTimeout(r, 100);

        "undefined" != typeof window && (t = requestAnimationFrame(r));
      })(F));
    }
  }, n.__c = function (t, r) {
    r.some(function (t) {
      try {
        t.__h.forEach(_$1), t.__h = t.__h.filter(function (n) {
          return !n.__ || g$1(n);
        });
      } catch (u) {
        r.some(function (n) {
          n.__h && (n.__h = []);
        }), r = [], n.__e(u, t.__v);
      }
    }), c$1 && c$1(t, r);
  }, n.unmount = function (t) {
    e$1 && e$1(t);
    var r = t.__c;

    if (r) {
      var u = r.__H;
      if (u) try {
        u.__.forEach(function (n) {
          return n.t && n.t();
        });
      } catch (t) {
        n.__e(t, r.__v);
      }
    }
  };

  var styles = {"button":"Button_button__3njfZ"};

  var Button = function Button(_ref) {
    var _ref$type = _ref.type,
        type = _ref$type === void 0 ? 'button' : _ref$type,
        className = _ref.className,
        onClick = _ref.onClick,
        disabled = _ref.disabled,
        children = _ref.children;
    return v("button", {
      type: type,
      className: [styles.button, className].join(' '),
      onClick: onClick,
      disabled: disabled
    }, children);
  };

  var styles$1 = {"container":"ScrollList_container__2zngD","content":"ScrollList_content__292u8","disabled":"ScrollList_disabled__3CYTK","button":"ScrollList_button__2wzhC","up":"ScrollList_up__acAn6"};

  var Segment = {
    PICKUP: 'pickup',
    DROPOFF: 'dropoff'
  };
  var Item = {
    HEIGHT: 50,
    // Scroll list item height (ie date or time slot)
    LARGE_SCREEN_COUNT: 4,
    // # items to display in scroll list for larger screens
    SMALL_SCREEN_COUNT: 4 // # items to display in scroll list for smaller screens

  };
  var MediaQuery = {
    LARGE_SCREEN: '(min-width: 960px)'
  };
  var DisplayMode = {
    DUAL: 'dual',
    // the default mode: a picker is shown for both segments, starting with the supplied segment.
    SINGLE: 'single' // a picker is shown only for the supplied segment. Used for rescheduling.

  };
  var SelectionMode = {
    SUBMIT: 'submit',
    AUTO: 'auto'
  };
  var PickerTitle = {
    PICKUP: 'Choose your collection time slot',
    DROPOFF: 'Choose your delivery time slot'
  };
  var TimeSlotTag = {
    ECO: 'eco'
  };

  var Chevron = function Chevron(_ref) {
    var direction = _ref.direction,
        color = _ref.color,
        props = _objectWithoutProperties(_ref, ["direction", "color"]);

    return v("svg", _extends({
      viewBox: "0 0 24 24",
      className: direction === 'up' ? styles$1.up : ''
    }, props), v("path", {
      d: "M18 9l-5.5147 5.4144L7 9.0288",
      stroke: color,
      strokeWidth: "1.2",
      fill: "none",
      fillRule: "evenodd"
    }));
  };

  var ScrollButton = function ScrollButton(_ref2) {
    var direction = _ref2.direction,
        color = _ref2.color,
        _onClick = _ref2.onClick;
    return v("div", {
      className: styles$1.button,
      onClick: function onClick() {
        return _onClick(direction);
      }
    }, v(Chevron, {
      direction: direction,
      color: color,
      height: 25
    }));
  };

  var ScrollList = function ScrollList(_ref3) {
    var children = _ref3.children,
        visibleItemCount = _ref3.visibleItemCount,
        currentIndex = _ref3.currentIndex,
        disabled = _ref3.disabled;
    var scrollRef = y$1(null);
    p(function () {
      var el = scrollRef.current;

      if (!el) {
        return;
      }

      var itemTop = currentIndex * Item.HEIGHT;
      var itemBottom = itemTop + Item.HEIGHT;
      var elTop = el.scrollTop;
      var elBottom = elTop + el.clientHeight;
      var nextTop = null;
      var isPartiallyVisible = false; // If the item is partially hidden, scroll it smoothly into view

      if (itemTop < elTop && itemBottom > elTop) {
        nextTop = itemTop;
        isPartiallyVisible = true;
      } else if (itemTop < elBottom && itemBottom > elBottom) {
        nextTop = elTop + (itemBottom - elBottom);
        isPartiallyVisible = true;
      } else if (itemBottom <= elTop || itemTop >= elBottom) {
        nextTop = itemTop;
      }

      if (nextTop !== null) {
        scrollRef.current.scroll({
          top: nextTop,
          left: 0,
          behavior: isPartiallyVisible ? 'smooth' : 'auto'
        });
      }
    }, [currentIndex]);

    var handleScrollClick = function handleScrollClick(direction) {
      var el = scrollRef.current;

      if (!el) {
        return;
      } // Item height is hardcoded


      var top = el.scrollTop;
      var nextTop;

      if (direction === 'up') {
        nextTop = Math.floor(top / Item.HEIGHT) * Item.HEIGHT;

        if (nextTop === top) {
          nextTop -= Item.HEIGHT;
        }
      } else {
        nextTop = Math.ceil(top / Item.HEIGHT) * Item.HEIGHT + Item.HEIGHT;
      }

      el.scroll({
        top: nextTop,
        left: 0,
        behavior: 'smooth'
      });
    };

    var buttonProps = {
      color: disabled ? '#ccc' : '#222',
      onClick: handleScrollClick
    };
    return v("div", {
      className: styles$1.container
    }, v(ScrollButton, _extends({
      direction: "up"
    }, buttonProps)), v("div", {
      ref: scrollRef,
      className: [styles$1.content, disabled ? styles$1.disabled : ''].join(' '),
      style: {
        height: Item.HEIGHT * visibleItemCount
      }
    }, children), v(ScrollButton, _extends({
      direction: "down"
    }, buttonProps)));
  };

  var styles$2 = {"container":"Picker_container__3a9RV","disabled":"Picker_disabled__2Oiwq","title":"Picker_title__2v8rC","picker":"Picker_picker__APANo","weekday":"Picker_weekday__zE6p7","date":"Picker_date__11_y_","time-slot":"Picker_time-slot__3e2yO","eco":"Picker_eco__2Cjid","eco-selected":"Picker_eco-selected__ovrY7","eco-text":"Picker_eco-text__33W-m","actions":"Picker_actions__1Lefw","left-button":"Picker_left-button__3t-XI","right-button":"Picker_right-button__bYroO","item":"Picker_item__3NjUU","selected":"Picker_selected__1AhjU","back":"Picker_back__3Vbb4"};

  var DateLabel = function DateLabel(_ref) {
    var weekday_label = _ref.weekday_label,
        date_label = _ref.date_label;
    return v(d, null, v("div", {
      className: styles$2.weekday
    }, weekday_label), v("div", {
      className: styles$2.date
    }, date_label));
  }; // Note: this uses hyphenated SVG attributes so it's not compatible with React


  var EcoSlotIcon = function EcoSlotIcon(_ref2) {
    var isSelected = _ref2.isSelected;
    return v("svg", {
      className: [styles$2.eco, isSelected ? styles$2['eco-selected'] : ''].join(' '),
      viewBox: "0 0 116 116"
    }, v("g", {
      fill: "none",
      "fill-rule": "evenodd"
    }, v("circle", {
      cx: "58",
      cy: "58",
      r: "55",
      stroke: "#00BF6C",
      "stroke-width": "4"
    }), v("g", {
      "stroke-linecap": "round",
      "stroke-linejoin": "round",
      "stroke-width": "3.6"
    }, v("path", {
      d: "M58.39 52.178L58.5 32M56.597 35.758c-2.5 2.362-7.476 1.256-11.123-2.476-3.643-3.728-4.57-8.676-2.07-11.037 2.493-2.367 7.475-1.257 11.117 2.47 3.648 3.734 4.574 8.676 2.076 11.043z"
    }), v("path", {
      d: "M60.406 35.758c2.498 2.362 7.474 1.256 11.12-2.476 3.643-3.728 4.569-8.676 2.07-11.037-2.493-2.367-7.474-1.257-11.115 2.47-3.648 3.734-4.58 8.676-2.075 11.043z"
    })), v("text", {
      className: styles$2['eco-text'],
      x: "22",
      y: "86"
    }, "ECO")));
  };

  var TimeSlotLabel = function TimeSlotLabel(_ref3, isSelected) {
    var label = _ref3.label,
        isEco = _ref3.isEco;
    return v(d, null, v("span", {
      className: styles$2['time-slot']
    }, label), isEco && v(EcoSlotIcon, {
      isSelected: isSelected
    }));
  };

  var PickList = function PickList(_ref4) {
    var options = _ref4.options,
        selectedValue = _ref4.value,
        onSelect = _ref4.onSelect,
        renderLabel = _ref4.renderLabel;
    return v(d, null, options.map(function (item, i) {
      var isSelected = selectedValue === item.value;
      return v("div", {
        key: item.value,
        onClick: function onClick() {
          return onSelect && onSelect(item.value, i);
        },
        className: [styles$2.item, isSelected ? styles$2.selected : ''].join(' ')
      }, renderLabel ? renderLabel(item, isSelected) : item.label);
    }));
  };

  var Placeholder = function Placeholder(_ref5) {
    var className = _ref5.className,
        title = _ref5.title,
        visibleItemCount = _ref5.visibleItemCount,
        options = _ref5.options;
    var dateOptions = [];
    var timeSlotOptions = [];

    if (options && options.length > 0) {
      dateOptions = options.slice(0, visibleItemCount);
      timeSlotOptions = dateOptions[0].timeSlots.slice(0, visibleItemCount);
    }

    return v("div", {
      className: [styles$2.container, styles$2.placeholder, className, styles$2.disabled].join(' ')
    }, v("div", {
      className: styles$2.title
    }, title), v("div", null, v("div", {
      className: styles$2.picker
    }, v(ScrollList, {
      visibleItemCount: visibleItemCount,
      disabled: true
    }, v(PickList, {
      options: dateOptions,
      renderLabel: DateLabel
    })), v(ScrollList, {
      visibleItemCount: visibleItemCount,
      disabled: true
    }, v(PickList, {
      options: timeSlotOptions
    })))), v("div", {
      className: styles$2.actions
    }));
  };

  var Picker = function Picker(_ref6) {
    var className = _ref6.className,
        title = _ref6.title,
        visibleItemCount = _ref6.visibleItemCount,
        options = _ref6.options,
        selectedIndexes = _ref6.selectedIndexes,
        onDateSelect = _ref6.onDateSelect,
        onTimeSlotSelect = _ref6.onTimeSlotSelect,
        leftButton = _ref6.leftButton,
        rightButton = _ref6.rightButton,
        _ref6$disabled = _ref6.disabled,
        disabled = _ref6$disabled === void 0 ? false : _ref6$disabled;

    // Prevent double submission
    var _useState = v$1(false),
        _useState2 = _slicedToArray(_useState, 2),
        hasClickedRightButton = _useState2[0],
        setRightButtonClicked = _useState2[1];

    var handleRightButtonClick = function handleRightButtonClick() {
      if (rightButton.once) {
        setRightButtonClicked(true);
      }

      rightButton.onClick();
    };

    var selectedDate = options[selectedIndexes.date];
    var timeSlotOptions = selectedDate.timeSlots;
    var selectedTimeSlot = timeSlotOptions[selectedIndexes.timeSlot];
    return v("div", {
      className: [styles$2.container, className, disabled ? styles$2.disabled : ''].join(' ')
    }, v("div", {
      className: styles$2.title
    }, title), v("div", {
      className: styles$2.picker
    }, v(ScrollList, {
      visibleItemCount: visibleItemCount,
      currentIndex: selectedIndexes.date,
      disabled: disabled
    }, v(PickList, {
      options: options,
      value: disabled ? null : selectedDate.value,
      onSelect: onDateSelect,
      renderLabel: DateLabel
    })), v(ScrollList, {
      visibleItemCount: visibleItemCount,
      currentIndex: selectedIndexes.timeSlot,
      disabled: disabled
    }, v(PickList, {
      options: timeSlotOptions,
      value: disabled ? null : selectedTimeSlot.value,
      onSelect: onTimeSlotSelect,
      renderLabel: TimeSlotLabel
    }))), v("div", {
      className: styles$2.actions
    }, !disabled && v(d, null, leftButton && !leftButton.isHidden && v(Button, {
      className: styles$2['left-button'],
      onClick: leftButton.onClick
    }, leftButton.text), rightButton && !rightButton.isHidden && v(Button, {
      className: styles$2['right-button'],
      onClick: handleRightButtonClick,
      disabled: hasClickedRightButton
    }, rightButton.text))));
  };

  Picker.Placeholder = Placeholder;

  var fetchAvailability = function fetchAvailability(url) {
    return fetch(url, {
      credentials: 'same-origin'
    }).then(function (response) {
      if (response.ok) {
        return response.json();
      }

      var error = new Error(response.statusText);
      var contentType = response.headers.get('Content-Type');

      if (contentType === 'application/json; charset=utf-8') {
        return response.json().then(function (data) {
          error.list = data.errors ? data.errors : [];
          throw error;
        });
      }

      throw error;
    });
  };

  var buildParams = function buildParams(baseParams, pickupSlot) {
    if (baseParams && (pickupSlot === undefined || !!pickupSlot)) {
      var params = _objectSpread2({}, baseParams);

      if (pickupSlot !== undefined && pickupSlot && !baseParams.pickup_start) {
        params.pickup_start = pickupSlot;
      }

      return params;
    }

    return null;
  };

  var buildUrl = function buildUrl(baseUrl, params) {
    var query = Object.keys(params).sort().map(function (key) {
      return "".concat(encodeURIComponent(key), "=").concat(encodeURIComponent(params[key]));
    }).join('&');
    return "".concat(baseUrl, "?").concat(query);
  }; // Public API


  var makeFetcher = function makeFetcher(baseUrl, baseParams, pickupSlot) {
    var params = buildParams(baseParams, pickupSlot);
    var url;
    var fetch;

    if (params) {
      url = buildUrl(baseUrl, params);
      fetch = function fetch() {
        return fetchAvailability(url);
      };
    } else {
      url = null;

      fetch = function fetch() {
        return Promise.reject('Invalid lookup');
      };
    }

    return {
      url: url,
      fetch: fetch,
      canFetch: !!url
    };
  };

  var useLockBodyScroll = function useLockBodyScroll(isLocked) {
    l(function () {
      if (!isLocked) {
        return;
      }

      var originalStyle = window.getComputedStyle(document.body).overflow;
      document.body.style.overflow = 'hidden';
      return function () {
        document.body.style.overflow = originalStyle;
      };
    }, [isLocked]);
  };

  var useMedia = function useMedia(query, defaultState) {
    var _useState = v$1(defaultState),
        _useState2 = _slicedToArray(_useState, 2),
        state = _useState2[0],
        setState = _useState2[1];

    p(function () {
      var mounted = true;
      var mediaQueryList = window.matchMedia(query);

      var handleChange = function handleChange() {
        if (!mounted) {
          return;
        }

        setState(Boolean(mediaQueryList.matches));
      };

      mediaQueryList.addListener(handleChange);
      setState(mediaQueryList.matches);
      return function () {
        mounted = false;
        mediaQueryList.removeListener(handleChange);
      };
    }, [query]);
    return state;
  };

  var usePrevious = function usePrevious(value) {
    var ref = y$1();
    p(function () {
      ref.current = value;
    });
    return ref.current;
  };

  var FALLBACK_ERROR = {
    code: 'unknown',
    detail: 'An unknown error occurred. Please try again or contact support.'
  }; // Return the first error or a generic error if the error
  // wasn't produced by the API

  var adaptError = function adaptError(error) {
    if (error.list && error.list.length) {
      return error.list[0];
    }

    return FALLBACK_ERROR;
  };

  var getOptions = function getOptions(availability, selectedValue) {
    var options = [];
    var selected;
    availability.forEach(function (_ref, dateIndex) {
      var time_slots = _ref.time_slots,
          dateItem = _objectWithoutProperties(_ref, ["time_slots"]);

      var timeSlots = [];
      time_slots.forEach(function (item, timeSlotIndex) {
        timeSlots.push(_objectSpread2({}, item, {
          isEco: item.tags.includes(TimeSlotTag.ECO)
        }));

        if (item.value === selectedValue || !selectedValue && item.is_default) {
          selected = {
            dateIndex: dateIndex,
            timeSlotIndex: timeSlotIndex,
            value: item.value
          };
        }
      });
      options.push(_objectSpread2({}, dateItem, {
        value: dateItem.date,
        timeSlots: timeSlots
      }));
    });

    if (!selected) {
      var dateIndex = 0;
      var timeSlotIndex = 0;
      selected = {
        dateIndex: dateIndex,
        timeSlotIndex: timeSlotIndex,
        value: options[dateIndex].timeSlots[timeSlotIndex].value
      };
    }

    return [options, selected];
  };

  var getSelection = function getSelection(state) {
    var selectedDate = state.options[state.dateIndex];

    if (!selectedDate) {
      return null;
    }

    var selectedTimeSlot = selectedDate.timeSlots[state.timeSlotIndex];
    return _objectSpread2({}, selectedTimeSlot, {
      date: selectedDate.value
    });
  };

  var reducer = function reducer(state, action) {
    switch (action.type) {
      case 'FETCH_REQUEST':
        return _objectSpread2({}, state, {
          url: action.url,
          isFetching: true,
          fetchError: null
        });

      case 'FETCH_SUCCESS':
        {
          var _getOptions = getOptions(action.availability, state.value),
              _getOptions2 = _slicedToArray(_getOptions, 2),
              options = _getOptions2[0],
              selected = _getOptions2[1];

          return _objectSpread2({}, state, {
            options: options,
            dateIndex: selected.dateIndex,
            timeSlotIndex: selected.timeSlotIndex,
            value: selected.value,
            isFetching: false,
            fetchCount: state.fetchCount + 1
          });
        }

      case 'FETCH_FAILURE':
        return _objectSpread2({}, state, {
          fetchError: adaptError(action.error),
          isFetching: false
        });

      case 'SELECT_DATE':
        {
          // Validate the selected time slot is still valid for the newly
          // selected date.
          var dateIndex = action.index;
          var nextTimeSlots = state.options[dateIndex].timeSlots;
          var selectedTimeSlot = getSelection(state);
          var nextTimeSlotIndex = nextTimeSlots.findIndex(function (ts) {
            return ts.label === selectedTimeSlot.label;
          });

          if (nextTimeSlotIndex === -1) {
            // If the time slot isn't available for the date, set it to
            // the latest time on that date.
            // TODO: would it be better to set it to a closer time?
            nextTimeSlotIndex = nextTimeSlots.length - 1;
          }

          var nextValue = nextTimeSlots[nextTimeSlotIndex].value;
          return _objectSpread2({}, state, {
            dateIndex: dateIndex,
            timeSlotIndex: nextTimeSlotIndex,
            value: nextValue
          });
        }

      case 'SELECT_TIME_SLOT':
        return _objectSpread2({}, state, {
          timeSlotIndex: action.index,
          value: action.value
        });

      default:
        throw new Error("Invalid action type: \"".concat(action.type, "\""));
    }
  };

  var useTimeSlot = function useTimeSlot(_ref2) {
    var availabilityFetcher = _ref2.availabilityFetcher,
        _ref2$initialValue = _ref2.initialValue,
        initialValue = _ref2$initialValue === void 0 ? null : _ref2$initialValue,
        _ref2$isDisabled = _ref2.isDisabled,
        isDisabled = _ref2$isDisabled === void 0 ? false : _ref2$isDisabled;

    var _useReducer = m$1(reducer, {
      url: null,
      isFetching: false,
      fetchError: null,
      fetchCount: 0,
      options: [],
      value: initialValue,
      dateIndex: null,
      timeSlotIndex: null
    }),
        _useReducer2 = _slicedToArray(_useReducer, 2),
        state = _useReducer2[0],
        dispatch = _useReducer2[1];

    var prevValue = usePrevious(state.value);
    var url = availabilityFetcher.url;
    p(function () {
      if (isDisabled || !availabilityFetcher.canFetch || url === state.url) {
        return;
      }

      dispatch({
        type: 'FETCH_REQUEST',
        url: url
      });
      availabilityFetcher.fetch().then(function (_ref3) {
        var availability = _ref3.availability;
        dispatch({
          type: 'FETCH_SUCCESS',
          availability: availability
        });
      }).catch(function (error) {
        dispatch({
          type: 'FETCH_FAILURE',
          error: error
        });
      });
    });

    var selectDate = function selectDate(value, index) {
      dispatch({
        type: 'SELECT_DATE',
        value: value,
        index: index
      });
    };

    var selectTimeSlot = function selectTimeSlot(value, index) {
      dispatch({
        type: 'SELECT_TIME_SLOT',
        value: value,
        index: index
      });
    };

    return {
      options: state.options,
      indexes: {
        date: state.dateIndex,
        timeSlot: state.timeSlotIndex
      },
      value: state.value,
      hasChanged: state.value !== prevValue,
      timeSlot: getSelection(state),
      selectDate: selectDate,
      selectTimeSlot: selectTimeSlot,
      error: state.fetchError,
      hasFetched: function hasFetched() {
        return state.fetchCount > 0;
      }
    };
  };

  var styles$3 = {"wrapper":"TimeSlotPicker_wrapper__35MsE","container":"TimeSlotPicker_container__3s45H","in-single-mode":"TimeSlotPicker_in-single-mode__1Syuo","pickup":"TimeSlotPicker_pickup__MchJu","dropoff":"TimeSlotPicker_dropoff__1X_jb"};

  var TimeSlotPicker = function TimeSlotPicker(_ref) {
    var _ref$displayMode = _ref.displayMode,
        displayMode = _ref$displayMode === void 0 ? DisplayMode.DUAL : _ref$displayMode,
        selectionMode = _ref.selectionMode,
        apiUrl = _ref.apiUrl,
        queryParams = _ref.queryParams,
        segment = _ref.segment,
        isVisible = _ref.isVisible,
        onSelect = _ref.onSelect,
        onSubmit = _ref.onSubmit,
        onClose = _ref.onClose,
        onError = _ref.onError,
        rightButtonText = _ref.rightButtonText,
        _ref$initialValues = _ref.initialValues,
        initialValues = _ref$initialValues === void 0 ? {} : _ref$initialValues;

    // Segment state
    var _useState = v$1(segment || Segment.PICKUP),
        _useState2 = _slicedToArray(_useState, 2),
        activeSegment = _useState2[0],
        setActiveSegment = _useState2[1];

    var lastSegment = usePrevious(segment);
    var pickupActive = activeSegment === Segment.PICKUP;
    var dropoffActive = !pickupActive;

    if (segment !== lastSegment && segment !== activeSegment) {
      // The caller wants to activate the inactive segment.
      // Set the state right away
      setActiveSegment(segment);
    } // UI state


    var inSingleDisplayMode = displayMode == DisplayMode.SINGLE;
    var forLargeScreen = useMedia(MediaQuery.LARGE_SCREEN, false);
    useLockBodyScroll(isVisible && !forLargeScreen);

    if (!selectionMode) {
      selectionMode = forLargeScreen ? SelectionMode.AUTO : SelectionMode.SUBMIT;
    }

    var inAutoSelectionMode = selectionMode === SelectionMode.AUTO;

    var shouldShowPicker = function shouldShowPicker(isSegmentActive) {
      return inSingleDisplayMode ? isSegmentActive : forLargeScreen || isSegmentActive;
    };

    var visibleItemCount = forLargeScreen ? Item.LARGE_SCREEN_COUNT : Item.SMALL_SCREEN_COUNT; // Time slot state

    var pickup = useTimeSlot({
      availabilityFetcher: makeFetcher(apiUrl, queryParams),
      initialValue: initialValues.pickup,
      isDisabled: inSingleDisplayMode && !pickupActive
    });
    var dropoff = useTimeSlot({
      availabilityFetcher: makeFetcher(apiUrl, queryParams, pickup.value),
      initialValue: initialValues.dropoff,
      isDisabled: !dropoffActive && !inAutoSelectionMode
    });

    var getEventPayload = function getEventPayload(segment) {
      return {
        segment: segment,
        timeSlot: segment === Segment.PICKUP ? pickup.timeSlot : dropoff.timeSlot,
        displayMode: displayMode,
        selectionMode: selectionMode
      };
    }; // Effects
    // TOOD: Are effects the best way to pass state to the library user?
    // Report errors to the widget caller


    p(function () {
      if (!onError) {
        return;
      }

      if (pickup.error) {
        onError({
          error: pickup.error,
          segment: Segment.PICKUP
        });
      } else if (dropoff.error) {
        onError({
          error: dropoff.error,
          segment: Segment.DROPOFF
        });
      }
    }, [onError, pickup.error, dropoff.error]); // Pass selected pickup time slot to caller

    p(function () {
      if (inAutoSelectionMode && pickup.timeSlot && pickup.hasChanged) {
        onSelect(getEventPayload(Segment.PICKUP));
        setActiveSegment(Segment.DROPOFF);
      } // FIXME: See if the below dependencies can be fixed
      // eslint-disable-next-line react-hooks/exhaustive-deps

    }, [onSelect, inAutoSelectionMode, pickup.value]); // Pass selected dropoff time slot to caller

    p(function () {
      if (inAutoSelectionMode && dropoff.timeSlot && dropoff.hasChanged) {
        onSelect(getEventPayload(Segment.DROPOFF));
      } // FIXME: See if the below dependencies can be fixed
      // eslint-disable-next-line react-hooks/exhaustive-deps

    }, [onSelect, inAutoSelectionMode, dropoff.value]);

    if (!isVisible || !inSingleDisplayMode && !pickup.hasFetched() || inSingleDisplayMode && dropoffActive && !dropoff.hasFetched()) {
      // We aren't ready to display anything yet
      return null;
    } // Event handlers


    var wrapPickupSelectHandler = function wrapPickupSelectHandler(handler) {
      return function () {
        handler.apply(void 0, arguments);
        setActiveSegment(Segment.PICKUP);
      };
    };

    var handlePickupSubmit = function handlePickupSubmit() {
      onSubmit(getEventPayload(Segment.PICKUP));

      if (!inSingleDisplayMode) {
        setActiveSegment(Segment.DROPOFF);
      }
    };

    var handleDropoffSubmit = function handleDropoffSubmit() {
      onSubmit(getEventPayload(Segment.DROPOFF));
    };

    var handleBackButtonClick = function handleBackButtonClick() {
      setActiveSegment(Segment.PICKUP);
    };

    return v("div", {
      className: styles$3.wrapper
    }, v("div", {
      className: [styles$3.container, inSingleDisplayMode ? styles$3['in-single-mode'] : ''].join(' ')
    }, shouldShowPicker(pickupActive) && (pickup.options.length > 0 ? v(Picker, {
      className: styles$3.pickup,
      title: PickerTitle.PICKUP,
      visibleItemCount: visibleItemCount,
      options: pickup.options,
      selectedIndexes: pickup.indexes,
      onDateSelect: wrapPickupSelectHandler(pickup.selectDate),
      onTimeSlotSelect: wrapPickupSelectHandler(pickup.selectTimeSlot),
      leftButton: onClose ? {
        onClick: onClose,
        text: 'Close'
      } : null,
      rightButton: {
        onClick: handlePickupSubmit,
        isHidden: !pickupActive || inAutoSelectionMode,
        text: 'Next'
      }
    }) : (!inSingleDisplayMode || pickupActive) && v(Picker.Placeholder, {
      className: styles$3.pickup,
      title: PickerTitle.PICKUP,
      visibleItemCount: visibleItemCount
    })), shouldShowPicker(dropoffActive) && (dropoff.options.length > 0 ? v(Picker, {
      className: styles$3.dropoff,
      title: PickerTitle.DROPOFF,
      visibleItemCount: visibleItemCount,
      options: dropoff.options,
      selectedIndexes: dropoff.indexes,
      onDateSelect: dropoff.selectDate,
      onTimeSlotSelect: dropoff.selectTimeSlot,
      disabled: !inAutoSelectionMode && !dropoffActive,
      leftButton: {
        onClick: inSingleDisplayMode && onClose ? onClose : handleBackButtonClick,
        isHidden: inSingleDisplayMode ? !inAutoSelectionMode : inAutoSelectionMode,
        text: inSingleDisplayMode ? 'Close' : 'Back'
      },
      rightButton: {
        onClick: handleDropoffSubmit,
        text: inAutoSelectionMode ? rightButtonText : 'Done',
        once: true
      }
    }) : v(Picker.Placeholder, {
      className: styles$3.dropoff,
      title: PickerTitle.DROPOFF,
      visibleItemCount: visibleItemCount,
      options: pickup.options
    }))));
  };

  var makePicker = function makePicker(container, props) {
    var initialProps = props;

    var renderPicker = function renderPicker(props) {
      // Queue render to avoid recursion issues
      window.setTimeout(function () {
        var picker = v(TimeSlotPicker, _extends({}, initialProps, props));
        E(picker, container);
      });
    };

    var _isVisible = false;
    return {
      configure: function configure(props) {
        initialProps = _objectSpread2({}, initialProps, {}, props);
      },
      select: function select(queryParams) {
        renderPicker({
          queryParams: queryParams,
          selectionMode: 'auto'
        });
      },
      show: function show(queryParams, segment) {
        _isVisible = true;
        renderPicker({
          queryParams: queryParams,
          segment: segment,
          isVisible: _isVisible
        });
      },
      hide: function hide() {
        _isVisible = false;
        renderPicker({
          isVisible: _isVisible
        });
      },
      isVisible: function isVisible() {
        return _isVisible;
      }
    };
  };

  return makePicker;

}());
