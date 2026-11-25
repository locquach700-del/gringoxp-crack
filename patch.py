import os, re

print("[*] GRINGOXP crack v6 - force main panel visible")

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
    print("[OK]", os.path.basename(path), sig.split("(")[0].split()[-1][:50])
    return True

def replace_method_by_name(path, name_token, body):
    with open(path, encoding="utf-8", errors="ignore") as f:
        c = f.read()
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
            with open(path, "w", encoding="utf-8") as f:
                f.write(c[:m] + body + c[end + len(".end method"):])
            print("[OK-name]", os.path.basename(path), name_token)
            return True
        idx = m + 8

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

            with open(p, encoding="utf-8", errors="ignore") as f:
                c = f.read()
            orig = c

            load_sig = "invoke-virtual {v1, v2, v0}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;Ljava/util/Map;)V"
            if load_sig in c:
                inject = (
                    load_sig + "\n\n"
                    "    # crack v6: hide login layout, show main panel\n"
                    "    const/16 v3, 0x8\n"
                    "    invoke-virtual {v1, v3}, Landroid/webkit/WebView;->setVisibility(I)V\n"
                    "    iget-object v4, v7, Lio/gringoxp/proxy/garena/freefire/LoginActivity;->C:Landroid/widget/LinearLayout;\n"
                    "    if-eqz v4, :cond_crack_skip\n"
                    "    invoke-virtual {v4, v3}, Landroid/view/View;->setVisibility(I)V\n"
                    "    :cond_crack_skip\n"
                    "    const/4 v3, 0x1\n"
                    "    iput-boolean v3, v7, Lio/gringoxp/proxy/garena/freefire/LoginActivity;->b0:Z\n"
                    "    const/4 v4, 0x0\n"
                    "    iput-boolean v4, v7, Lio/gringoxp/proxy/garena/freefire/LoginActivity;->e0:Z\n"
                    "    sput-boolean v3, Lp/Ag;->l:Z\n"
                    "    sput-boolean v3, Lp/Ag;->m:Z\n"
                    "    iget-object v5, v7, Lio/gringoxp/proxy/garena/freefire/LoginActivity;->A:Landroid/widget/LinearLayout;\n"
                    "    if-eqz v5, :cond_crack_skip2\n"
                    "    invoke-virtual {v5, v4}, Landroid/view/View;->setVisibility(I)V\n"
                    "    :cond_crack_skip2\n"
                    "    invoke-virtual {v7}, Lio/gringoxp/proxy/garena/freefire/LoginActivity;->E()V\n"
                    "    invoke-virtual {v7}, Lio/gringoxp/proxy/garena/freefire/LoginActivity;->D()V\n"
                )
                c = c.replace(load_sig, inject, 1)
                print("[OK] inject hide C show A")
                n += 1

            if c != orig:
                open(p, "w", encoding="utf-8").write(c)

        if name == "Ag.smali":
            with open(p, encoding="utf-8", errors="ignore") as f:
                c = f.read()
            if "Lp/Ag" in c[:300] and "sput-boolean v0, Lp/Ag;->l:Z" not in c:
                marker = ".method static synthetic constructor <clinit>()V"
                start = c.find(marker)
                if start != -1:
                    nextm = c.find("\n.method ", start + 10)
                    if nextm == -1:
                        nextm = len(c)
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
                        print("[OK] Ag.l/m true")
                        n += 1

print(f"[*] total: {n}")
print("[*] Done")
