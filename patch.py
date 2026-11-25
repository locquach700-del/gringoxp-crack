import os, re

print("[*] GRINGOXP crack v4 - login invalid key fix")

def replace_method(path, sig, body):
    with open(path, encoding="utf-8", errors="ignore") as f:
        c = f.read()
    start = c.find(sig)
    if start == -1:
        return False
    nextm = c.find("\n.method ", start + 10)
    if nextm == -1:
        nextm = len(c)
    end = c.rfind(".end method", start, nextm)
    if end == -1:
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(c[:start] + body + c[end + len(".end method"):])
    print("[OK]", os.path.basename(path), sig.split("(")[0].split()[-1][:40])
    return True

def replace_method_by_name(path, name_token, body):
    """Find .method line containing name_token and replace whole method."""
    with open(path, encoding="utf-8", errors="ignore") as f:
        c = f.read()
    # find .method ... name_token
    idx = 0
    while True:
        m = c.find(".method ", idx)
        if m == -1:
            return False
        line_end = c.find("\n", m)
        header = c[m:line_end]
        if name_token in header:
            nextm = c.find("\n.method ", m + 10)
            if nextm == -1:
                nextm = len(c)
            end = c.rfind(".end method", m, nextm)
            if end == -1:
                return False
            # keep access flags from original if body starts with .method
            with open(path, "w", encoding="utf-8") as f:
                f.write(c[:m] + body + c[end + len(".end method"):])
            print("[OK-name]", os.path.basename(path), name_token)
            return True
        idx = m + 8
    return False

STR_REPLACEMENTS = [
    ("N\u00e3o foi poss\u00edvel preparar o aplicativo. Confira a instala\u00e7\u00e3o.", "Pronto."),
    ("Não foi possível preparar o aplicativo. Confira a instalação.", "Pronto."),
    ("Arquivo do aplicativo ausente ou inv\u00e1lido.", "OK."),
    ("Arquivo do aplicativo ausente ou inválido.", "OK."),
    ("Chave de acesso inv\u00e1lida.", "OK"),
    ("Chave de acesso inválida.", "OK"),
    ("Chave de acesso inv\u00e1lida", "OK"),
    ("chave de acesso inv\u00e1lida", "OK"),
    ("Invalid access key", "OK"),
    ("invalid key", "OK"),
    ("Key inv\u00e1lida", "OK"),
    ("Key inválida", "OK"),
    # force web login to blank so server cannot reject
    ("https://ff.gringoxp.site/dashboard?version=13", "about:blank"),
    ("https://ff.gringoxp.site/index?version=13", "about:blank"),
]

n = 0
for root, dirs, files in os.walk("."):
    for name in files:
        if not name.endswith(".smali"):
            continue
        p = os.path.join(root, name)

        if name == "LicenseSession.smali":
            if replace_method(p,
                ".method public static declared-synchronized accept(Ljava/lang/String;Ljava/lang/String;)Z",
                ".method public static declared-synchronized accept(Ljava/lang/String;Ljava/lang/String;)Z\n    .registers 2\n    const/4 v0, 0x1\n    return v0\n.end method\n"):
                n += 1
            if replace_method(p,
                ".method public static declared-synchronized begin(Landroid/content/Context;Ljava/lang/String;)Z",
                ".method public static declared-synchronized begin(Landroid/content/Context;Ljava/lang/String;)Z\n    .registers 2\n    const/4 v0, 0x1\n    return v0\n.end method\n"):
                n += 1
            if replace_method(p,
                ".method public static permissions()I",
                ".method public static permissions()I\n    .registers 1\n    const/4 v0, -0x1\n    return v0\n.end method\n"):
                n += 1

        if name == "LicenseSignature.smali":
            if replace_method(p,
                ".method public static verify([BLjava/lang/String;[B)Z",
                ".method public static verify([BLjava/lang/String;[B)Z\n    .registers 3\n    const/4 v0, 0x1\n    return v0\n.end method\n"):
                n += 1

        if name == "UpdateActivity.smali":
            if replace_method(p,
                ".method public final installBundledModule(Ljava/lang/String;Ljava/lang/String;)Z",
                ".method public final installBundledModule(Ljava/lang/String;Ljava/lang/String;)Z\n    .registers 3\n    const/4 v0, 0x1\n    return v0\n.end method\n"):
                n += 1
            if replace_method_by_name(p, "nativeUpdate(",
                ".method public nativeUpdate(Ljava/lang/String;)Z\n    .registers 2\n    const/4 v0, 0x1\n    return v0\n.end method\n"):
                n += 1

        if name == "LoginActivity.smali":
            if replace_method_by_name(p, "isNativeInjectionAuthorized",
                ".method private isNativeInjectionAuthorized()Z\n    .registers 1\n    const/4 v0, 0x1\n    return v0\n.end method\n"):
                n += 1

        # WebViewClient - auto accept any navigation / page finish
        if name in ("rb.smali", "Rb.smali"):
            # force shouldOverrideUrlLoading to return false (allow) or true after grant
            if replace_method_by_name(p, "shouldOverrideUrlLoading",
                ".method public final shouldOverrideUrlLoading(Landroid/webkit/WebView;Landroid/webkit/WebResourceRequest;)Z\n    .registers 3\n    const/4 v0, 0x0\n    return v0\n.end method\n"):
                n += 1
            if replace_method_by_name(p, "shouldOverrideUrlLoading",
                ".method public final shouldOverrideUrlLoading(Landroid/webkit/WebView;Ljava/lang/String;)Z\n    .registers 3\n    const/4 v0, 0x0\n    return v0\n.end method\n"):
                n += 1

        # Ag.l / Ag.m = true at class load
        if name == "Ag.smali" and "Lp/Ag" in open(p, encoding="utf-8", errors="ignore").read()[:200]:
            with open(p, encoding="utf-8", errors="ignore") as f:
                c = f.read()
            # inject at end of <clinit> before return-void: sput-boolean 1 to l and m
            if "sput-boolean" not in c[c.find("<clinit>"):c.find("<clinit>")+500] or True:
                marker = ".method static synthetic constructor <clinit>()V"
                if marker in c:
                    # find first return-void of clinit and insert before it
                    start = c.find(marker)
                    nextm = c.find("\n.method ", start + 10)
                    if nextm == -1: nextm = len(c)
                    # find last return-void before end method of clinit
                    endm = c.rfind(".end method", start, nextm)
                    ret = c.rfind("return-void", start, endm)
                    if ret != -1:
                        inject = (
                            "    const/4 v0, 0x1\n"
                            "    sput-boolean v0, Lp/Ag;->l:Z\n"
                            "    sput-boolean v0, Lp/Ag;->m:Z\n"
                        )
                        c = c[:ret] + inject + c[ret:]
                        open(p, "w", encoding="utf-8").write(c)
                        print("[OK] Ag.l/m forced true")
                        n += 1

        # string replacements
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                c = f.read()
            orig = c
            for old, new in STR_REPLACEMENTS:
                if old in c:
                    c = c.replace(old, new)
            if c != orig:
                open(p, "w", encoding="utf-8").write(c)
                print("[STR]", os.path.basename(p))
                n += 1
        except Exception:
            pass

print(f"[*] total patches: {n}")
print("[*] Done")
