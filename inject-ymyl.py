#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
subaog.com — 品牌 YMYL 信任信号注入 (参考台湾站 subao.tw 改编)
给 en/about + zh-cn/about 注入完整 Organization + AboutPage schema:
founders(创始团队/12年物流+8年报关)、foundingDate、areaServed、contactPoint、
priceRange、sameAs(同源台湾站)、资质(award)
"""
import re
import json
from pathlib import Path

ROOT = Path(".")

ORG_ZH = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "速豹回国物流",
    "alternateName": "Subao Global Logistics",
    "url": "https://subaog.com",
    "logo": "https://subaog.com/assets/images/logo.png",
    "description": "专注各国到中国的回国行李专线服务，覆盖美国、日本、韩国、欧洲、澳洲、加拿大、东南亚。空运 7-12 天、海运 25-35 天门到门，双清包税，比国际快递便宜 40-60%。",
    "foundingDate": "2020",
    "founders": [{
        "@type": "Person",
        "name": "速豹创始团队",
        "description": "12 年国际物流经验（前大型货代跨境线主管）+ 8 年报关与供应链管理经验，专注跨境物流合规操作",
    }],
    "areaServed": [
        {"@type": "Country", "name": "United States"},
        {"@type": "Country", "name": "Japan"},
        {"@type": "Country", "name": "South Korea"},
        {"@type": "Country", "name": "Australia"},
        {"@type": "Country", "name": "Canada"},
        {"@type": "Country", "name": "United Kingdom"},
    ],
    "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer service",
        "availableLanguage": ["Chinese", "English"],
        "email": "info@subaog.com",
    },
    "priceRange": "$5.5-$9.5/kg",
    "sameAs": ["https://subao.tw"],
    "award": ["12 年跨境物流经验", "双清包税专线", "正规报关资质"],
}

ORG_EN = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Subao Global Logistics",
    "alternateName": "速豹回国物流",
    "url": "https://subaog.com",
    "logo": "https://subaog.com/assets/images/logo.png",
    "description": "Door-to-door return-luggage and consolidation shipping to China from the US, Japan, Korea, Europe, Australia, Canada and Southeast Asia. Air 7-12 days, sea 25-35 days, tax-inclusive, 40-60% cheaper than international express.",
    "foundingDate": "2020",
    "founders": [{
        "@type": "Person",
        "name": "Subao Founding Team",
        "description": "12 years of international logistics plus 8 years of customs and supply-chain experience, focused on compliant cross-border operations.",
    }],
    "areaServed": [
        {"@type": "Country", "name": "United States"},
        {"@type": "Country", "name": "Japan"},
        {"@type": "Country", "name": "South Korea"},
        {"@type": "Country", "name": "Australia"},
        {"@type": "Country", "name": "Canada"},
        {"@type": "Country", "name": "United Kingdom"},
    ],
    "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer service",
        "availableLanguage": ["Chinese", "English"],
        "email": "info@subaog.com",
    },
    "priceRange": "$5.5-$9.5/kg",
    "sameAs": ["https://subao.tw"],
    "award": ["12+ years cross-border shipping", "Tax-inclusive door-to-door line", "Licensed customs clearance"],
}


def build_about(lang):
    org = ORG_ZH if lang == "zh-cn" else ORG_EN
    return {
        "@context": "https://schema.org",
        "@type": "AboutPage",
        "name": "关于速豹回国物流" if lang == "zh-cn" else "About Subao Global Logistics",
        "url": f"https://subaog.com/{lang}/about",
        "mainEntity": org,
    }


def inject(rel):
    f = ROOT / rel
    t = f.read_text(encoding="utf-8", errors="ignore")
    lang = "zh-cn" if rel.startswith("zh-cn/") else "en"
    # 幂等: 已含 Organization 的完整 founders 则跳过
    if '"founders"' in t and '"foundingDate"' in t:
        return "skip"
    org_ld = '<script type="application/ld+json">' + json.dumps(ORG_ZH if lang == "zh-cn" else ORG_EN, ensure_ascii=False) + "</script>"
    about_ld = '<script type="application/ld+json">' + json.dumps(build_about(lang), ensure_ascii=False) + "</script>"
    # 删除旧的弱 AboutPage schema(若有)
    t = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema.org",\s*"@type":\s*"AboutPage".*?</script>', "", t, flags=re.S)
    t = t.replace("</head>", org_ld + "\n" + about_ld + "\n</head>", 1)
    f.write_text(t, encoding="utf-8")
    return "done"


def main():
    for rel in ["en/about.html", "zh-cn/about.html"]:
        r = inject(rel)
        print(f"  {'✅' if r=='done' else '•跳过(已有)'} {rel}")


if __name__ == "__main__":
    main()
