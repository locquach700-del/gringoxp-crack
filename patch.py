import os, glob, re

print("[*] GRINGOXP crack v2")

def replace_method(path, sig, body):
    with open(path) as f:
        c = f.read()
    start = c.find(sig)
    if start == -1:
        print("[SKIP]", os.path.basename(path), sig[:60])
        return False
    nextm = c.find("\n.method ", start + 10)
    if nextm == -1:
        nextm = len(c)
    end = c.rfind(".end method", start, nextm)
    if end == -1:
        return False
    with open(path, "w") as f:
        f.write(c[:start] + body + c[end + len(".end method"):])
    print("[OK]", os.path.basename(path), sig.split("(")[0].split()[-1])
    return True

for root, dirs, files in os.walk("."):
    for name in files:
        if not name.endswith(".smali"):
            continue
        p = os.path.join(root, name)

        if name == "LicenseSession.smali":
            replace_method(p,
                ".method public static declared-synchronized accept(Ljava/lang/String;Ljava/lang/String;)Z",
                ".method public static declared-synchronized accept(Ljava/lang/String;Ljava/lang/String;)Z\n    .registers 2\n    const/4 v0, 0x1\n    return v0\n.end method\n")
            replace_method(p,
                ".method public static declared-synchronized begin(Landroid/content/Context;Ljava/lang/String;)Z",
                ".method public static declared-synchronized begin(Landroid/content/Context;Ljava/lang/String;)Z\n    .registers 2\n    const/4 v0, 0x1\n    return v0\n.end method\n")
            replace_method(p,
                ".method public static permissions()I",
                ".method public static permissions()I\n    .registers 1\n    const/4 v0, -0x1\n    return v0\n.end method\n")

        if name == "LicenseSignature.smali":
            replace_method(p,
                ".method public static verify([BLjava/lang/String;[B)Z",
                ".method public static verify([BLjava/lang/String;[B)Z\n    .registers 3\n    const/4 v0, 0x1\n    return v0\n.end method\n")

        # Fix "Não foi possível preparar o aplicativo" - module install fails crypto check
        if name == "UpdateActivity.smali":
            replace_method(p,
                ".method public final installBundledModule(Ljava/lang/String;Ljava/lang/String;)Z",
                ".method public final installBundledModule(Ljava/lang/String;Ljava/lang/String;)Z\n    .registers 3\n    const/4 v0, 0x1\n    return v0\n.end method\n")

print("[*] Done")
