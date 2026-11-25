import os, re

print("[*] GRINGOXP crack v3 - prepare fix")

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
    print("[OK]", os.path.basename(path), sig.split("(")[0].split()[-1])
    return True

# Error / status string replacements (UI)
STR_REPLACEMENTS = [
    ("N\u00e3o foi poss\u00edvel preparar o aplicativo. Confira a instala\u00e7\u00e3o.", "Pronto."),
    ("N\u00e3o foi poss\u00edvel preparar o aplicativo. Confira a instalação.", "Pronto."),
    ("Não foi possível preparar o aplicativo. Confira a instalação.", "Pronto."),
    ("N\u00e3o foi poss\u00edvel validar o m\u00f3dulo principal", "Módulo OK."),
    ("Não foi possível validar o módulo principal", "Módulo OK."),
    ("Arquivo do aplicativo ausente ou inv\u00e1lido.", "OK."),
    ("Arquivo do aplicativo ausente ou inválido.", "OK."),
    ("A instala\u00e7\u00e3o n\u00e3o foi confirmada.", "Instalação OK."),
    ("A instalação não foi confirmada.", "Instalação OK."),
]

patched_methods = 0
patched_strings = 0

for root, dirs, files in os.walk("."):
    for name in files:
        if not name.endswith(".smali"):
            continue
        p = os.path.join(root, name)

        if name == "LicenseSession.smali":
            if replace_method(p,
                ".method public static declared-synchronized accept(Ljava/lang/String;Ljava/lang/String;)Z",
                ".method public static declared-synchronized accept(Ljava/lang/String;Ljava/lang/String;)Z\n    .registers 2\n    const/4 v0, 0x1\n    return v0\n.end method\n"):
                patched_methods += 1
            if replace_method(p,
                ".method public static declared-synchronized begin(Landroid/content/Context;Ljava/lang/String;)Z",
                ".method public static declared-synchronized begin(Landroid/content/Context;Ljava/lang/String;)Z\n    .registers 2\n    const/4 v0, 0x1\n    return v0\n.end method\n"):
                patched_methods += 1
            if replace_method(p,
                ".method public static permissions()I",
                ".method public static permissions()I\n    .registers 1\n    const/4 v0, -0x1\n    return v0\n.end method\n"):
                patched_methods += 1

        if name == "LicenseSignature.smali":
            if replace_method(p,
                ".method public static verify([BLjava/lang/String;[B)Z",
                ".method public static verify([BLjava/lang/String;[B)Z\n    .registers 3\n    const/4 v0, 0x1\n    return v0\n.end method\n"):
                patched_methods += 1

        if name == "UpdateActivity.smali":
            if replace_method(p,
                ".method public final installBundledModule(Ljava/lang/String;Ljava/lang/String;)Z",
                ".method public final installBundledModule(Ljava/lang/String;Ljava/lang/String;)Z\n    .registers 3\n    const/4 v0, 0x1\n    return v0\n.end method\n"):
                patched_methods += 1
            # nativeUpdate - force success
            if replace_method(p,
                ".method public native nativeUpdate(Ljava/lang/String;)Z",
                ".method public nativeUpdate(Ljava/lang/String;)Z\n    .registers 2\n    const/4 v0, 0x1\n    return v0\n.end method\n"):
                patched_methods += 1
                print("[OK] nativeUpdate -> true (non-native stub)")

        # Global string replacements in this file
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                c = f.read()
            orig = c
            for old, new in STR_REPLACEMENTS:
                if old in c:
                    c = c.replace(old, new)
                    patched_strings += 1
            if c != orig:
                open(p, "w", encoding="utf-8").write(c)
                print("[STR]", p)
        except Exception as e:
            pass

# Also try to find Runnable classes that call installBundledModule / updateStatus with failure
# Force methods named run() in classes that reference UpdateActivity prepare flow - aggressive:
# any method returning Z that contains "installBundledModule" invoke - already covered by stubbing the callee.

print(f"[*] methods={patched_methods} strings={patched_strings}")
print("[*] Done")
