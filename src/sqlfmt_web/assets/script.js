!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
posthog.init('phc_JvcbkJ52TJpVaMxGHRGOxYrcOuTKU05949sLeVp8r7g',{api_host:'https://app.posthog.com'})
function set_theme(new_theme, old_theme) {
    document.documentElement.setAttribute('data-theme', new_theme);
    localStorage.setItem('theme', new_theme);
    var code_themes = {
        'light': 'cm-s-default',
        'dark': 'cm-s-base16-dark',
    };
    codemirror_textarea = document.getElementsByClassName("CodeMirror CodeMirror-wrap")[0];
    for(t in code_themes) {
        codemirror_textarea.classList.remove(code_themes[t]);
    }
    codemirror_textarea.classList.add(code_themes[new_theme]);
};
function toggle_theme() {
    current_theme = document.documentElement.getAttribute('data-theme');
    if (current_theme == 'dark') {
        new_theme = 'light'
    } else {
        new_theme = 'dark'
    };
    set_theme(new_theme, current_theme)
};
function get_theme_from_storage() {
    return localStorage.getItem("theme")
};
