# High-Ticket Expert Growth System — Başlangıç Rehberi

> Bu rehber, sistemi ilk kez kullananlar için yazılmıştır. Kurulumdan gerçek iş kararlarına kadar tüm senaryoları örneklerle ele alır.

---

## İçindekiler

- [Bu Sistem Ne Yapar?](#bu-sistem-ne-yapar)
- [Kurulum](#kurulum)
- [İlk Adım: business_context.yaml'ı Doldurmak](#i̇lk-adım-business_contextyamli-doldurmak)
- [Senaryo 1 — Sıfırdan Pazar Seçmek](#senaryo-1--sıfırdan-pazar-seçmek)
- [Senaryo 2 — Avatar ve Acı Araştırması](#senaryo-2--avatar-ve-acı-araştırması)
- [Senaryo 3 — Yüksek Biletli Teklif Tasarlamak](#senaryo-3--yüksek-biletli-teklif-tasarlamak)
- [Senaryo 4 — Değer Yığını ve Fiyatlandırma](#senaryo-4--değer-yığını-ve-fiyatlandırma)
- [Senaryo 5 — Müşteri Kazanım Stratejisi](#senaryo-5--müşteri-kazanım-stratejisi)
- [Senaryo 6 — Otorite İçerik Planı](#senaryo-6--otorite-i̇çerik-planı)
- [Senaryo 7 — Satış Hunisi Haritası](#senaryo-7--satış-hunisi-haritası)
- [Senaryo 8 — Satış Senaryosu ve İtiraz Yönetimi](#senaryo-8--satış-senaryosu-ve-i̇tiraz-yönetimi)
- [Senaryo 9 — Meta Reklam Yönetimi](#senaryo-9--meta-reklam-yönetimi)
- [Senaryo 10 — VSL (Video Satış Mektubu) Yazmak](#senaryo-10--vsl-video-satış-mektubu-yazmak)
- [Senaryo 11 — Müşteri Vaka Çalışması](#senaryo-11--müşteri-vaka-çalışması)
- [Senaryo 12 — YouTube Kanal Stratejisi](#senaryo-12--youtube-kanal-stratejisi)
- [Senaryo 13 — Lansman Kampanyası Planlamak](#senaryo-13--lansman-kampanyası-planlamak)
- [Senaryo 14 — Pazar Araştırması ve Rakip Takibi](#senaryo-14--pazar-araştırması-ve-rakip-takibi)
- [Senaryo 15 — İş Puan Kartı ve Darboğaz Tespiti](#senaryo-15--i̇ş-puan-kartı-ve-darboğaz-tespiti)
- [Senaryo 16 — Yeni Agent Eklemek](#senaryo-16--yeni-agent-eklemek)
- [Senaryo 17 — Tam Döngü: Sıfırdan Ölçeğe](#senaryo-17--tam-döngü-sıfırdan-ölçeğe)
- [Dashboard Kullanımı](#dashboard-kullanımı)
- [Kalite ve Test Komutları](#kalite-ve-test-komutları)
- [Sık Yapılan Hatalar](#sık-yapılan-hatalar)

---

## Bu Sistem Ne Yapar?

Bu sistem, uzmanlığını yüksek biletli (high-ticket) bir işe dönüştürmek isteyen profesyoneller için tasarlanmış **yerel, modüler bir AI agent fabrikasıdır**.

**Hedef kullanıcı örnekleri:**

- Danışmanlık yapan bir finans uzmanı → müşteri kazanım sistemini otomatize etmek istiyor
- Kurs satmaya başlayan bir fitness koçu → teklifini ve satış huniyi yapılandırmak istiyor
- Freelancer olmaktan çıkıp ajans kurmak isteyen bir dijital pazarlamacı
- Bilgisini paketleyip online satmak isteyen herhangi bir uzman

**Sistem şunları yapmaz:**
- ChatGPT gibi sohbet robotu değildir
- API anahtarı gerektirmez (mock/yerel modda tamamen çalışır)
- Otomatik karar almaz; her strateji güncellemesi insan onayı ister

**Sistem şunları yapar:**
- Pazar → Avatar → Teklif → Kanıt → Kazanım → Satış → Teslimat → Tutundurma → Ölçek zincirini aşama aşama işler
- Her aşama için yapılandırılmış Markdown çıktılar üretir
- Araştırma sinyallerini kaynağa dayalı depolar, referans ister
- Etik kuralları sistem düzeyinde uygular (sahte iddia, sahte referans, sahte kıtlık yok)

---

## Kurulum

```bash
# Repoyu klonla
git clone https://github.com/kullaniciadi/agent-dev-boilerplate.git
cd agent-dev-boilerplate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Sistem sağlıklı mı kontrol et
python -m pytest

# Agent yapısını doğrula
python scripts/validate_agent_structure.py

# Dashboard'u başlat (isteğe bağlı)
python dashboard/server.py
# Tarayıcıda aç: http://localhost:8765
```

Herhangi bir API anahtarı gerekmez. Sistem mock modda tamamen çalışır.

---

## İlk Adım: business_context.yaml'ı Doldurmak

`business_context.yaml` sistemin beynidir. Tüm agent'lar bu dosyadan okur.

**Kurallar:**
- Bilmediğin alanları boş bırak (sistem "bilinmiyor" olarak etiketler)
- Tahminleri not alanına yaz
- Gerçek olmayan iddia ekleme

### Örnek: Fitness Koçu

```yaml
{
  "expert": {
    "niche": "online fitness coaching for busy professionals",
    "expertise": "strength training and habit formation",
    "years_experience": "7",
    "credibility_assets": ["NSCA-CPT sertifikası", "500+ müşteri", "Transformasyon fotoğrafları"],
    "audience_size": "8000 Instagram takipçisi",
    "current_channels": ["Instagram", "e-posta listesi"],
    "delivery_strengths": ["birebir koçluk", "grup programları"],
    "unique_experience": "9-5 çalışırken 35 kilo verdim ve 6 yıldır koruyorum"
  },
  "market": {
    "market_name": "online fitness coaching",
    "urgency_level": "yüksek — sağlık sorunu veya görünüm kaygısı",
    "ability_to_pay": "orta-yüksek — kurumsal çalışanlar",
    "competitors": ["Caliber", "Future", "yerel gym koçları"]
  },
  "customer": {
    "target_customer": "35-50 yaş kurumsal çalışan",
    "specific_avatar": "Mehmet, 42, yazılım yöneticisi, haftada 60+ saat çalışıyor, 15 kilo fazlası var, daha önce 3 diyeti bıraktı",
    "main_problem": "disiplinli kalmak için zamanı ve enerjisi yok",
    "expensive_problem": "sağlık sorunları ve enerji eksikliği kariyer ve aile hayatını etkiliyor",
    "dream_outcome": "6 ayda 15 kilo vermek, sabahları enerjik uyanmak",
    "objections": ["zamanım yok", "daha önce denemedim olmadı", "çok pahalı"]
  },
  "offer": {
    "current_offer": "3 aylık birebir online koçluk programı",
    "current_price": "3000 TL",
    "core_promise": "90 günde minimum 8 kilo, ya da para iadesi",
    "guarantee": "90 gün sonuç garantisi"
  }
}
```

### Örnek: B2B Danışman

```yaml
{
  "expert": {
    "niche": "SaaS şirketleri için müşteri başarısı danışmanlığı",
    "expertise": "churn azaltma ve NPS iyileştirme",
    "years_experience": "12",
    "credibility_assets": ["Türkiye'nin ilk 3 unicorn'unda CSO görevleri", "2 yayınlanan vaka çalışması"],
    "current_channels": ["LinkedIn", "referanslar"],
    "unique_experience": "Churn'ü %34'ten %8'e indirdiğim 3 şirket var"
  },
  "customer": {
    "target_customer": "10-100 çalışanlı SaaS şirketi kurucusu",
    "expensive_problem": "yüksek churn şirket değerini düşürüyor, yatırımcı güvenini sarsıyor",
    "dream_outcome": "12 ayda churn'ü yarıya indirmek, ARR'yi %40 büyütmek"
  },
  "offer": {
    "current_price": "15000 USD",
    "current_offer": "6 aylık CS dönüşüm programı"
  }
}
```

---

## Senaryo 1 — Sıfırdan Pazar Seçmek

**Durum:** Birden fazla niş fikrin var ama hangisini seçeceğini bilmiyorsun.

**Kullanılan agent:** `market_selector`

**Adımlar:**

```bash
# Pazar puan kartını çalıştır
python scripts/generate_market_scorecard.py \
  --agent market_selector \
  --context business_context.yaml
```

**Çıktı:** `outputs/market_scorecards/` klasörüne bir Markdown raporu üretir.

**Rapor şunları içerir:**
- Pazar acı skoru (1-10)
- Ödeme gücü değerlendirmesi
- Ulaşılabilirlik notu
- Rekabet yoğunluğu analizi
- Genel pazar skoru

### Gerçek Kullanım Örneği

Diyelim ki üç pazar fikrin var:
1. Online İngilizce eğitimi
2. SaaS şirketleri için LinkedIn outreach ajansı
3. E-ticaret mağazaları için reklam yönetimi

`business_context.yaml`'a her birini sırayla gir, puan kartını çalıştır, karşılaştır.

**İyi pazar sinyalleri:**
- İnsanlar bu problemi çözmek için zaten para harcıyor
- Problem, ertelenmesi pahalıya patlayan türden
- Hedef kitleye ulaşmak mümkün (LinkedIn, YouTube, özel topluluklar)
- Rakipler var ama hiçbiri net lider değil

**Kötü pazar sinyalleri:**
- Herkes "harika fikir" diyor ama kimse para ödemiyor
- Hedef kitle dağınık ve ulaşılamıyor
- Problem bir lüks, zorunluluk değil

```bash
# Agent'ı doğrudan sorgulamak için
python scripts/run_agent.py \
  --agent market_selector \
  --message "Online İngilizce koçluğu ile SaaS LinkedIn outreach ajansı arasında seçim yapıyorum. Hangisi daha güçlü bir pazar?"
```

---

## Senaryo 2 — Avatar ve Acı Araştırması

**Durum:** Pazarı seçtin ama müşterini net tanımlamıyorsun. "Herkes hedef kitlem" tuzağına düşmek istemiyorsun.

**Kullanılan agent:** `avatar_pain_researcher`

**Adımlar:**

```bash
python scripts/generate_avatar_research.py \
  --agent avatar_pain_researcher \
  --context business_context.yaml
```

**Çıktı:** `outputs/avatar_research/` → spesifik avatar profili, acı haritası, satın alma tetikleyicileri, müşteri dili örnekleri.

### Örnek: Koçluk İşi

**Zayıf avatar (kaçın):**
> "30-50 yaş arası çalışan kadınlar"

**Güçlü avatar:**
> "Ayşe, 38, İstanbul'da orta düzey yönetici, 2 çocuğu var. Sabah 7'de ofiste, akşam 7'de evde. Her ay biri diyete başlayıp biri bitiyor. Temel korkusu: 40'a geldiğinde annesi gibi şeker hastası olmak. Pazar sabahı kahvaltısında diyetisyen Instagram'larına bakıyor ama hiçbirinin 'onun gibi' biri olmadığını düşünüyor."

Bu avatar tanımıyla yazdığın içerik, reklam ve satış senaryosu çok daha spesifik olur.

### Araştırma ile Avatar Doğrulamak

```bash
# Reddit'ten gerçek müşteri dili topla
python scripts/collect_source.py \
  --source reddit \
  --query "busy professional struggling to lose weight"

# Rakip reklamları analiz et
python scripts/collect_source.py \
  --source facebook_ad_library \
  --query "online fitness coaching"

# Çapraz kaynak analizi
python scripts/analyze_cross_source_signals.py
```

Toplanan sinyaller `research/sources/` altına kaydedilir. Her sinyal kaynakla etiketlenir; tek kaynaktan gelen sinyal "aday", birden fazla kaynaktan doğrulanmış sinyal "doğrulanmış" olarak işaretlenir.

---

## Senaryo 3 — Yüksek Biletli Teklif Tasarlamak

**Durum:** Avatar'ın net. Şimdi onların gerçekten satın alacağı bir teklif tasarlaman gerekiyor.

**Kullanılan agent:** `offer_architect`

**Adımlar:**

```bash
python scripts/generate_offer_audit.py \
  --agent offer_architect \
  --context business_context.yaml
```

**Çıktı:** `outputs/offer_audits/` → teklif güçlü/zayıf yönleri, mekanizma netliği, değer denklemine göre değerlendirme.

### Teklif Anatomisi

Sistem teklifinizi şu beş boyutta değerlendirir (Hormozi'nin değer denklemi):

| Boyut | Soru | Örnek |
|---|---|---|
| **Sonuç** | Müşteri ne elde ediyor? | 90 günde 12 kilo |
| **Olasılık** | Müşteri başarıya ne kadar inanıyor? | 3 müşteri vaka çalışması |
| **Süre** | Ne kadar sürede? | 90 gün, haftada 3 saat |
| **Efor** | Ne kadar çaba gerekiyor? | Sadece alışveriş listesi ve 30 dk antrenman |
| **Risk** | Sonuç gelmezse ne olur? | Tam iade garantisi |

### Örnek: Zayıf vs. Güçlü Teklif

**Zayıf:**
> "3 aylık online fitness koçluğu — 3000 TL"

**Güçlü:**
> "Meşgul Profesyoneller İçin 90 Günlük Vücut Dönüşüm Programı: Haftada 3x30 dakika ile 8-15 kilo ver, ya da her kuruşunu iade ederim. 23 müşteriden 21'i hedefine ulaştı."

Sistem şunları sorgular:
- Mekanizma spesifik mi ve kopyalanamaz mı?
- İddialar desteklenmiş mi?
- Risk tersine çevrilmiş mi?
- Aceleyi meşrulaştıran bir neden var mı?

```bash
# Teklifle ilgili spesifik soru sor
python scripts/run_agent.py \
  --agent offer_architect \
  --message "Teklifimde garantiyi nasıl güçlendiririm? Şu an '90 gün sonuç yoksa iade' var ama kimse ciddiye almıyor."
```

---

## Senaryo 4 — Değer Yığını ve Fiyatlandırma

**Durum:** Teklifin var ama fiyatı nasıl belirleyeceğini ve değer algısını nasıl yükselteceğini bilmiyorsun.

**Kullanılan agentlar:** `value_stack_builder`, `pricing_guarantee_optimizer`

**Adımlar:**

```bash
# Değer yığını oluştur
python scripts/generate_value_stack.py \
  --agent value_stack_builder \
  --context business_context.yaml

# Fiyatlandırma ve garanti değerlendirmesi
python scripts/generate_pricing_guarantee_review.py \
  --agent pricing_guarantee_optimizer \
  --context business_context.yaml
```

### Değer Yığını Örneği

Diyelim ki online fitness koçluğu satıyorsun. 3000 TL fiyatı "pahalı" hissettiriyor çünkü değer yığını eksik.

**Zayıf teklif paketi:**
- 3 aylık koçluk: 3000 TL

**Güçlü değer yığını:**

| Eleman | Algılanan Değer |
|---|---|
| 12 haftalık kişiselleştirilmiş program | 2400 TL |
| Haftalık 1:1 check-in çağrıları (12 seans) | 1800 TL |
| Kişisel beslenme planı | 600 TL |
| WhatsApp destek erişimi | 900 TL |
| **Bonus:** Alışveriş listesi ve meal-prep rehberi | 300 TL |
| **Bonus:** Yolculuk antrenman paketi | 200 TL |
| **Garanti:** 90 günde 8 kilo yoksa tam iade | Sınırsız |
| **Toplam algılanan değer** | **6200 TL** |
| **Gerçek fiyat** | **3000 TL** |

Sistem şunları kontrol eder:
- Fiyat pazar benchmarklarına uygun mu?
- Ödeme planı seçeneği olmalı mı?
- Garanti türü (sonuç garantisi mi, memnuniyet mi, karma mı?) doğru seçilmiş mi?

### Fiyatlandırma Rehberi

```
Düşük bilet: 1000 TL altı → volüm gerekir, birebir ölçeklenmez
Orta bilet: 1000-10.000 TL → karma ölçek mümkün
Yüksek bilet: 10.000 TL+ → az müşteri, yüksek dönüşüm gerekir
```

Sistem, fiyatı müşterinin "pahalı bir problem" yaşayıp yaşamadığına göre değerlendirir.

---

## Senaryo 5 — Müşteri Kazanım Stratejisi

**Durum:** Teklifin hazır. Şimdi potansiyel müşteri nereden gelecek?

**Kullanılan agent:** `acquisition_strategy_agent`

**Adımlar:**

```bash
python scripts/generate_acquisition_plan.py \
  --agent acquisition_strategy_agent \
  --context business_context.yaml
```

**Çıktı:** `outputs/acquisition_plans/` → haftalık kazanım aksiyonları, kanal öncelikleri, maliyet-fayda değerlendirmesi.

### Kazanım Kanalları

Sistem şu kanalları değerlendirir:

| Kanal | Avantajı | Dezavantajı |
|---|---|---|
| **Organik içerik** (LinkedIn, Instagram) | Ücretsiz, otorite inşa eder | Yavaş, tutarlılık ister |
| **Ücretli reklamlar** (Meta, Google) | Hızlı, ölçeklenebilir | Bütçe gerektirir, kırılgan |
| **Outbound** (DM, e-posta) | Anında, kontrollü | Emek yoğun |
| **Ortaklıklar** | Leverage, güven transferi | İlişki kurma süresi |
| **Topluluk** (webinar, etkinlik) | Yüksek güven | Uzun dönemli |
| **Referans** | En yüksek kapanma oranı | Başlangıçta az |

### Örnek: B2B Danışman İçin Kazanım Planı

```bash
python scripts/run_agent.py \
  --agent acquisition_strategy_agent \
  --message "SaaS şirketleri için CS danışmanlığı yapıyorum. Henüz hiç reklam vermedim, LinkedIn profilim var ama aktif değilim. Haftada 10 saatim var. Nereden başlamalıyım?"
```

**Sistem önerisi (örnek çıktı):**
1. LinkedIn profilini 72 saatte optimize et (hedef kitleye yönelik başlık ve özet)
2. Hafta 1-4: Günlük 1 içerik (müşteri dönüşüm hikayesi, churn insight, Q&A)
3. Haftada 15 hedefli DM: "CS ekibinizi nasıl yapılandırdığınızı merak ettim…"
4. Ay 2: Bir webinar: "SaaS'ta Churn Azaltmanın 3 Matematik Hatası"
5. Ay 3: İlk müşteriden referans sistemi kur

---

## Senaryo 6 — Otorite İçerik Planı

**Durum:** Nişinde otorite olmak istiyorsun ama ne içerik üreteceğini bilmiyorsun.

**Kullanılan agent:** `content_authority_agent`

**Adımlar:**

```bash
python scripts/generate_content_plan.py \
  --agent content_authority_agent \
  --context business_context.yaml
```

**Çıktı:** `outputs/content_plans/` → içerik kategorileri, örnek başlıklar, yayın takvimi.

### İçerik Kategorileri

Sistem içeriği beş amaca göre organize eder:

| Kategori | Amaç | Örnek |
|---|---|---|
| **Otorite** | "Bu konuyu biliyor" algısı | "12 yılda 47 danışman müşteriden öğrendiğim şey" |
| **Kanıt** | Gerçek sonuçlar | "Mehmet, 42: 90 günde 14 kilo nasıl verdi?" |
| **İtiraz** | Engelleri kaldır | "Zamanın olmadığı için değil, sistem kurmadığın için" |
| **Talep Yaratma** | Farkındalık aç | "Şeker hastalarının %80'i 40'tan önce uyarı alıyordu" |
| **CTA** | Harekete geçir | "90 günlük programım için 5 yer kaldı" |

### Örnek İçerik Takvimi (Haftalık)

| Gün | Tür | Örnek Başlık |
|---|---|---|
| Pazartesi | Otorite | Sektörden karşı-sezgisel bir insight |
| Çarşamba | Kanıt | Müşteri hikayesi (rakamlarla) |
| Cuma | İtiraz | En yaygın itirazı ele al |
| Pazar | Kişisel | Senin hikayenden bir sahne |

---

## Senaryo 7 — Satış Hunisi Haritası

**Durum:** İçeriğin var, ama potansiyel müşterileri nasıl toplayacağın ve satışa taşıyacağın belli değil.

**Kullanılan agent:** `funnel_builder`

**Adımlar:**

```bash
python scripts/generate_funnel_map.py \
  --agent funnel_builder \
  --context business_context.yaml
```

**Çıktı:** `outputs/funnel_maps/` → lead magnet önerisi, uygulama hunisi, e-posta sırası, webinar/workshop planı.

### Huni Akışı Örneği

```
FARKINDALILIK
  └── Instagram reels / LinkedIn makaleleri
        ↓
LEAD MAGNET (bedava değer)
  └── "Meşgul Profesyoneller İçin 7 Günlük Hızlı Başlangıç Rehberi" (PDF)
        ↓
E-POSTA SERİSİ (7-10 e-posta)
  └── E-posta 1: Hoş geldin + rehber
  └── E-posta 3: Mehmet'in hikayesi (vaka çalışması)
  └── E-posta 5: "Neden diyet çalışmıyor?" (itiraz içeriği)
  └── E-posta 7: Programın açıklaması
  └── E-posta 9: Başvuru daveti
        ↓
BAŞVURU FORMU
  └── Sağlık durumu, hedef, bütçe sorularıyla ön nitelendirme
        ↓
KEŞIF ÇAĞRISI (15-20 dk)
  └── Fit mi değil mi? → Devam et
        ↓
SATIŞ ÇAĞRISI (45-60 dk)
  └── Karar
```

### Lead Magnet Seçimi

```bash
python scripts/run_agent.py \
  --agent funnel_builder \
  --message "SaaS CS danışmanlığı için hangi lead magnet en iyi çalışır? Webinar mı, PDF rehber mi, yoksa ücretsiz audit mi?"
```

Sistem her seçeneği şu kriterlere göre puanlar: teslim kolaylığı, nitelendirme değeri, algılanan değer, hızlı kazanım potansiyeli.

---

## Senaryo 8 — Satış Senaryosu ve İtiraz Yönetimi

**Durum:** Keşif çağrıları yapıyorsun ama kapama oranın düşük ya da itirazlarla nasıl başa çıkacağını bilmiyorsun.

**Kullanılan agentlar:** `sales_script_builder`, `objection_handler`

**Adımlar:**

```bash
# Satış senaryosu
python scripts/generate_sales_script.py \
  --agent sales_script_builder \
  --context business_context.yaml

# İtiraz bankası
python scripts/generate_objection_bank.py \
  --agent objection_handler \
  --context business_context.yaml
```

### Satış Çağrısı Yapısı

Sistem etik bir satış çağrısı için beş aşama üretir:

```
1. RAPOR KURMA (5 dk)
   — Neden bu çağrıya katıldıklarını sor

2. KEŞİF (15-20 dk)
   — Şu anda neredesiniz?
   — Bu değişmeseydi 1 yıl sonra ne olurdu?
   — Daha önce ne denediniz?
   — Bu sorunu çözmek sizi nereye götürür?

3. TEKLİF SUNUMU (10 dk)
   — Programı anlat
   — Adım adım ne olacağını göster

4. KARAR ÇERÇEVELEME (5 dk)
   — "Bu sizin için mantıklı görünüyor mu?"
   — İtirazları dinle ve ele al

5. SONUÇ (5 dk)
   — Net bir sonuca ulaş
   — Takip planını belirle
```

### İtiraz Bankası Örnekleri

| İtiraz | Etik Yanıt |
|---|---|
| "Çok pahalı" | "Bütçe mi kısıtlayıcı yoksa değer konusunda belirsizlik mi var?" |
| "Zamanım yok" | "Bu program haftada kaç saatinizi alıyor dersiniz?" |
| "Eşimle konuşmam lazım" | "Tabii ki. Bu kararı birlikte almak için sizi yarın arayabilir miyim?" |
| "Önce biraz düşüneyim" | "Tabii. Ne üzerinde düşünmek istediğinizi sorabilir miyim?" |

---

## Senaryo 9 — Meta Reklam Yönetimi

**Durum:** Organik büyüme yavaş, reklamla hızlanmak istiyorsun ama Meta reklamlarında kayboluyorsun.

**Kullanılan agent:** `meta_ads_manager`

**Adımlar:**

```bash
python scripts/generate_meta_ads_plan.py \
  --agent meta_ads_manager \
  --context business_context.yaml
```

**Çıktı:** `outputs/meta_ads_plans/` → kampanya yapısı, creative brief'leri, P.D.A. matrisi, bütçe önerileri.

### Andromeda-First Yaklaşım

Bu agent'ın temel felsefesi Meta'nın kendi açıkladığı gerçeğe dayanır: **"Creative IS targeting."** Andromeda (Meta'nın AI motoru) kime reklam göstereceğini senin hedefleme ayarlarından değil, creative içeriğinden öğrenir.

**Yanlış yaklaşım:**
- Dar kitle hedefleme (25-35, İstanbul, fitness ilgisi, spor salonu gitmiş)
- 2-3 creative varyant
- Haftalık kampanya değişiklikleri

**Doğru yaklaşım:**
- Geniş hedefleme (sadece dil + coğrafya)
- 15-20 kavramsal olarak farklı creative
- Öğrenme fazını koru: 50 dönüşüme kadar dokunma

### P.D.A. Creative Matrisi

Her creative üç boyutta farklılaşmalı:

| Boyut | Seçenekler |
|---|---|
| **P — Persona** | Bütçe odaklı, statü odaklı, kolaylık odaklı, başlangıç seviyesi, uzman, şüpheci |
| **D — Arzu** | Hız, tasarruf, statü, güven, dönüşüm, kolaylık |
| **A — Farkındalık** | Problem farkında, çözüm farkında, ürün farkında |

**Örnek Creative Briefingi:**

```
Creative #1: Persona=Başlangıç, Arzu=Hız, Farkındalık=Problem
Hook: "3 diyeti bıraktıysanız bu sizin hatanız değil"
Format: UGC tarzı telefon videosu
CTA: "Sistemi gör"

Creative #2: Persona=Uzman, Arzu=Dönüşüm, Farkındalık=Ürün
Hook: "Neden 90 gün garanti veriyorum?"
Format: Talking head, stüdyo
CTA: "Başvur"
```

### Haftalık Reklam Döngüsü

```
PAZARTESİ: Metrikler gözden geçir (CTR, CPL, kalite sıralaması)
ÇARŞAMBA: Öğrenme fazı tamamlananları değerlendir
CUMA: Yeni creative brief hazırla
PAZARTESİ: Yeni creative'leri yükle
```

**Dokunma kuralları:**
- Öğrenme fazında olan kampanyaya DOKUNMA
- Bütçeyi %20'den fazla bir seferde değiştirme
- Creative değiştirme ≠ kitle değiştirme

---

## Senaryo 10 — VSL (Video Satış Mektubu) Yazmak

**Durum:** Satış sayfan ya da reklam videolarında izleyiciyi satışa taşıyacak güçlü bir script istiyorsun.

**Kullanılan agent:** `vsl_copywriter`

**Adımlar:**

```bash
python scripts/generate_vsl_script.py \
  --agent vsl_copywriter \
  --context business_context.yaml
```

**Çıktı:** `outputs/vsl_scripts/` → beş fazlı VSL scripti, landing page taslağı.

### VSL'nin 5 Fazı

```
FAZ 1 — PROFİLLEME
  Senaryo: Kim için? → Tek bir spesifik kişiyi seç
  Örnek: "Bu video sadece 35-50 yaş, haftada 50+ saat çalışan ve daha önce en az iki diyeti bırakan kişiler için"

FAZ 2 — AÇILIŞ (İlk 30 saniye kritik)
  Hook: Acı veya paradoks
  Örnek: "Dünyanın her yerinde araştırmalar aynı şeyi söylüyor: disiplin sorunu değil, sistem sorunu. Ve bugün size o sistemi göstereceğim."

FAZ 3 — TEKLİF
  — Problem → Pahalı hale getir → Çözüm sun
  — Rakiplerden farkını bir cümleyle söyle (mekanizma)
  — Değer yığınını görsel olarak listele

FAZ 4 — KAPANIŞ
  — Fiyatı değer yığınından sonra aç
  — Garantiyi net ifade et
  — Kıtlık/aciliyet (gerçekse): "Bu ay 5 yer kaldı"

FAZ 5 — LANDING PAGE YAPISI
  — Headline: Kimin için + sonuç + süre
  — Sosyal kanıt: Vaka çalışmaları
  — CTA: Net bir eylem
```

---

## Senaryo 11 — Müşteri Vaka Çalışması

**Durum:** Müşterilerinden harika sonuçlar aldın ama bunu nasıl içeriğe dönüştüreceğini bilmiyorsun.

**Kullanılan agent:** `case_study_writer`

**Adımlar:**

```bash
python scripts/generate_case_study.py \
  --agent case_study_writer \
  --context business_context.yaml
```

**Çıktı:** `outputs/case_studies/` → Hormozi tarzı yüksek dönüşümlü vaka çalışması.

### Hormozi Vaka Çalışması Formatı

Vague hikayeler güven yaratmaz. Spesifik rakamlar güven yaratır.

**Zayıf:**
> "Mehmet ile çalıştık ve çok memnun kaldı."

**Güçlü:**
```
BAŞLIK: "42 yaşında yazılım müdürü Mehmet, 
         91 günde 14.3 kilo verdi ve sabah 5:30'da uyanmaya başladı"

BAŞLANGIÇ DURUMU:
- Mehmet, 87 kg, 174 cm
- Önceki 4 yılda 3 farklı diyet: ortalama 6 hafta sonra bırakmış
- Günlük enerji: "akşam toplantılara zor giriyorum"

MÜDAHALEMİZ:
- 12 haftalık kişisel program
- Haftada 3x30 dk antrenman (toplantı öncesi 7:00-7:30)
- Haftalık check-in her Pazartesi 8:00

SONUÇLAR (91. gün):
- Ağırlık: 87 kg → 72.7 kg (−14.3 kg)
- Sabah kalkma saati: 07:30 → 05:30
- Müşteri yorumu: "İlk kez bir programı bitirdim"

ANAHTAR KARAR: 
"Pazartesi sabahı toplantıdan önce spor yapınca motivasyon 
toplantıya girdi — akşam yapıyordum, her zaman iptal ediyordum"
```

**Kurallara dikkat:**
- Gerçek olmayan rakam kullanma
- Müşteri onayı al
- "Tipik sonuç değildir" disclaimerını ekle

---

## Senaryo 12 — YouTube Kanal Stratejisi

**Durum:** YouTube'da niş otoritesi olmak istiyorsun ama nasıl başlayacağını bilmiyorsun.

**Kullanılan agent:** `youtube_strategy_agent`

**Adımlar:**

```bash
python scripts/generate_youtube_strategy.py \
  --agent youtube_strategy_agent \
  --context business_context.yaml
```

**Çıktı:** `outputs/youtube_strategies/` → kanal stratejisi, SEO planı, içerik takvimi.

### Turanlı Method'un Özü

Bu agent, SEO-first, AI-destekli faceless (yüzsüz) prodüksiyon yaklaşımıyla çalışır.

**Temel prensipler:**
1. Kanal ilk günden nişe yönelik olmalı
2. Her video bir arama terimi etrafında inşa edilmeli
3. Title > Thumbnail (önce başlık kur, sonra thumbnail tasarla)
4. İlk 48 saat abone tabanına push → algoritma kararı orada verilir

**İçerik Türleri:**

| Tür | Amaç | Frekans |
|---|---|---|
| **Evergreen SEO** | Uzun vadeli arama trafiği | Haftada 2-3 |
| **Trend** | Kısa vadeli patlama | Fırsata göre |
| **Otorite** | "Bu adamı takip etmeliyim" | Ayda 2 |

**Örnek Kanal Planı (Fitness Koç):**

```
Hafta 1-4: Temel SEO videoları
  — "Evde 30 dakika ile nasıl kilo verilir" (çok aranan)
  — "Sabah mı akşam mı antrenman daha iyi" (tartışmalı = tıklama)
  — "Diyet yapmadan kilo verdiren 5 alışkanlık"

Hafta 5-8: Otorite videoları
  — "42 yaşında 14 kilo veren müşterimin hikayesi"
  — "Neden çoğu fitness koçu yanlış öğretiyor"

Sürekli: Topluluk tabanlı
  — "Sorularınızı yanıtlıyorum" formatı
```

---

## Senaryo 13 — Lansman Kampanyası Planlamak

**Durum:** Yeni bir program ya da ürün piyasaya çıkarmak istiyorsun. Haftalarca sürecek bir lansman sürecini nasıl yöneteceğini bilmiyorsun.

**Kullanılan agent:** `launch_campaign_manager`

**Adımlar:**

```bash
python scripts/generate_launch_campaign.py \
  --agent launch_campaign_manager \
  --context business_context.yaml
```

**Çıktı:** `outputs/launch_campaigns/` → ön lansman planı, sepet açık/kapanış takvimi, e-posta dizisi, reklam planı, lansman debrifi.

### Lansman Takvimi Örneği (4 Haftalık)

```
HAFTA 1 — ÖN LANSMAN: Farkındalık
  — İçerik: Avatar'ın acılarını işle
  — E-posta: "Yakında büyük bir şey geliyor" + beklenti listesi
  — Reklam: Traffic kampanyası, video görüntüleme

HAFTA 2 — ÖN LANSMAN: Değer Teslimi
  — İçerik: Ücretsiz mini eğitim (YouTube, canlı)
  — E-posta: Vaka çalışması serisi (3 e-posta)
  — Reklam: Retargeting başlat (video izleyenlere)

HAFTA 3 — SEPET AÇIK (5-7 gün)
  — E-posta Günlük (launch sequence):
    — Gün 1: Açılış + değer
    — Gün 2: Vaka çalışması
    — Gün 3: İtirazları ele al
    — Gün 4: Soru-cevap
    — Gün 5: Son gün bildirimi
    — Gün 6: Kapanış e-postası (sabah + akşam)
  — Reklam: Dönüşüm kampanyası, retargeting ağırlıklı

HAFTA 4 — DEBRİF
  — Satış rakamlarını not al
  — Nelerin çalışmadığını belgele
  — Sıradaki lansmanı planla
```

---

## Senaryo 14 — Pazar Araştırması ve Rakip Takibi

**Durum:** Pazarın gerçekten ne düşündüğünü, rakiplerin ne söylediğini öğrenmek istiyorsun.

**Adımlar:**

```bash
# Reddit'ten müşteri dili topla
python scripts/collect_source.py \
  --source reddit \
  --query "online coaching scam expensive"

# Facebook reklam kütüphanesinden rakip reklamları
python scripts/collect_source.py \
  --source facebook_ad_library \
  --query "online fitness coaching Turkey"

# Google Trends ile talep yönü
python scripts/collect_source.py \
  --source google_trends \
  --query "online koçluk"

# YouTube ile içerik trendleri
python scripts/collect_source.py \
  --source youtube \
  --query "high ticket coaching funnel"

# Rakip web sitelerini analiz et
python scripts/monitor_competitors.py \
  --query "online fitness coaching Turkey"

# Tüm sinyalleri çapraz analiz et
python scripts/analyze_cross_source_signals.py
```

### Araştırma Güven Sistemi

Her araştırma sinyali otomatik etiketlenir:

| Durum | Anlam | Aksiyon |
|---|---|---|
| `candidate` | Tek kaynaktan geldi | Strateji kararı verme |
| `validated` | Birden fazla kaynaktan doğrulandı | Strateji güncelleme için kullanabilirsin |
| `is_mock: true` | Gerçek veriye bakma, mock | Test ortamında göz ardı et |

**Önemli kural:** Mock araştırma sinyallerini gerçek pazar verisi gibi kullanma. Sistem bunu zorla etiketler.

### Haftalık Araştırma Döngüsü

```bash
# Tek komutla tüm haftalık araştırmayı çalıştır
python scripts/run_weekly_research.py
```

Bu komut şunları yapar:
1. Tüm etkin kaynakları toplar
2. Sinyalleri işler
3. Çapraz kaynak raporu üretir
4. Tüm referansları `research/index/collected_references.jsonl`'e yazar

---

## Senaryo 15 — İş Puan Kartı ve Darboğaz Tespiti

**Durum:** İşin hangi aşamasında takıldığını anlamak istiyorsun.

**Kullanılan agent:** `business_scorecard_agent`

**Adımlar:**

```bash
python scripts/generate_business_scorecard.py \
  --agent business_scorecard_agent \
  --context business_context.yaml
```

**Çıktı:** `outputs/business_scorecards/` → darboğaz analizi, öncelik sırası, haftanın bir numaralı odak noktası.

### Darboğaz Tespiti

Sistem şu aşamaları puanlar:

```
TRAFIK: Yeterli potansiyel müşteri geliyor mu?
  ↓
LEAD KALITE: Gelen kişiler doğru avatar mı?
  ↓
BAŞVURU: Başvuru formu yeterince nitelendiriyor mu?
  ↓
GÖSTER: Çağrılara katılım oranı nedir?
  ↓
KAPAMA: Satış çağrısında kaçta kaçı kapatıyorsun?
  ↓
TESLİMAT: Müşteriler sonuç alıyor mu?
  ↓
TUTUNDURMA: Yeniden satın alıyor / referans veriyor mu?
```

**Örnek Darboğaz Teşhisi:**

```
Trafik: 1000 kişi/ay → İYİ
Lead kalite: %60 doğru avatar → ORTA
Başvuru: %8 form dolduruyor → ZAYIF ← DARBOĞAZ BURASI
Görüşme: %70 katılıyor → İYİ
Kapama: %30 kapanıyor → ORTA

Öneri: Başvuru formunu nitelendirme soruları ekleyerek güçlendir.
       Lead magnet ile daha iyi filtrele.
```

---

## Senaryo 16 — Yeni Agent Eklemek

**Durum:** Mevcut agent'lar yetmiyor, sisteme özel bir agent eklemek istiyorsun.

**Örnek:** Satış sayfası yazım agent'ı eklemek.

```bash
# Şablondan yeni agent oluştur
python scripts/create_agent.py \
  --name sales_page_reviewer \
  --role "Sales Page Reviewer"
```

Bu komut şu dosyaları otomatik oluşturur:

```
agents/sales_page_reviewer/
  agent.yaml              ← Konfigürasyon
  system_prompt.md        ← Agent davranışı (bunu yaz)
  checklist.yaml          ← Kalite kontrol kuralları
  knowledge/              ← Agent'a özel bilgi
  memory/                 ← Konuşma belleği
  outputs/                ← Üretilen dosyalar
```

**Ardından:**

1. `system_prompt.md` dosyasını düzenle → agent'ın rolünü, çalışma prensiplerini, çıktı formatını yaz
2. `checklist.yaml`'a kalite kurallarını ekle
3. `agent.yaml`'da izin verilen araçları belirle
4. Test et:

```bash
python scripts/run_agent.py \
  --agent sales_page_reviewer \
  --message "Bu satış sayfasını incele: [URL ya da metin]"
```

**Checklist:**
- Mock modda çalışıyor mu?
- Sahte iddia üretmiyor mu?
- Çıktı formatı tanımlı mı?
- Eval case'leri yazıldı mı?

```bash
python scripts/validate_agent_structure.py
python -m pytest
```

---

## Senaryo 17 — Tam Döngü: Sıfırdan Ölçeğe

Bu senaryo, tüm sistemi sırayla kullanan bir uzmanın tam yolculuğunu gösterir.

### Kullanılan Profil

> **Zeynep, 34, serbest çalışan UX tasarımcısı**
> 8 yıldır freelance yapıyor, saatlik 150 TL alıyor. Gelirini katlamak ve daha az ama daha değerli müşteriyle çalışmak istiyor. Hedefi: 6 ayda 3x aylık gelir.

---

### Hafta 1-2: Temel Kurulum

```bash
# 1. Projeyi kur
pip install -r requirements.txt

# 2. business_context.yaml'ı doldur
# niche: "UX danışmanlığı SaaS startup'ları için"
# avatar: "B2B SaaS kurucusu, kullanıcı kaybediyor ama nedenini bilmiyor"
# offer: "UX audit + roadmap paketi"
# price: "5000 TL"

# 3. Pazar değerlendir
python scripts/generate_market_scorecard.py \
  --agent market_selector \
  --context business_context.yaml

# 4. Avatar derinleştir
python scripts/generate_avatar_research.py \
  --agent avatar_pain_researcher \
  --context business_context.yaml
```

**Bulgu:** Sistem, SaaS startup'larının UX sorununun "pahalı problem" kategorisinde olduğunu doğruluyor: kötü UX = yüksek churn = yatırımcı sorunu.

---

### Hafta 3-4: Teklif ve Fiyat

```bash
# 5. Teklifi güçlendir
python scripts/generate_offer_audit.py \
  --agent offer_architect \
  --context business_context.yaml

# 6. Değer yığını oluştur
python scripts/generate_value_stack.py \
  --agent value_stack_builder \
  --context business_context.yaml

# 7. Fiyatlandırmayı optimize et
python scripts/generate_pricing_guarantee_review.py \
  --agent pricing_guarantee_optimizer \
  --context business_context.yaml
```

**Bulgu:** 5000 TL fiyat çok düşük; pazar benchmarkları ve "pahalı problem" analizi 15.000-25.000 TL aralığını destekliyor. Sistem değer yığını eklemesini öneriyor.

**Yeni teklif paketi:**
- UX Audit (2 hafta) → 8000 TL algılanan değer
- Öncelikli İyileştirme Roadmap → 5000 TL
- 3 aylık uygulama desteği → 6000 TL
- Kullanıcı testi kolaylaştırması → 3000 TL
- **Toplam algılanan değer: 22.000 TL**
- **Gerçek fiyat: 15.000 TL**

---

### Hafta 5-6: Kazanım ve İçerik

```bash
# 8. Kazanım stratejisi
python scripts/generate_acquisition_plan.py \
  --agent acquisition_strategy_agent \
  --context business_context.yaml

# 9. İçerik planı
python scripts/generate_content_plan.py \
  --agent content_authority_agent \
  --context business_context.yaml

# 10. LinkedIn ve Reddit araştırması
python scripts/collect_source.py \
  --source reddit \
  --query "SaaS UX problems user retention"
```

**Öncelikli kanal:** LinkedIn (B2B SaaS kurucuları LinkedIn'de)
**İlk 30 günlük plan:**
- Günlük 1 LinkedIn içerik (UX hatası analizi, vaka, Q&A)
- Haftada 10 hedefli DM: "Ürününüzün onboarding akışında bir gözlemim var…"

---

### Hafta 7-8: Huni ve Satış

```bash
# 11. Huni haritası
python scripts/generate_funnel_map.py \
  --agent funnel_builder \
  --context business_context.yaml

# 12. Satış senaryosu
python scripts/generate_sales_script.py \
  --agent sales_script_builder \
  --context business_context.yaml

# 13. İtiraz bankası
python scripts/generate_objection_bank.py \
  --agent objection_handler \
  --context business_context.yaml
```

---

### Ay 3+: Reklam, Kanıt ve Ölçek

```bash
# 14. İlk müşteri vaka çalışması
python scripts/generate_case_study.py \
  --agent case_study_writer \
  --context business_context.yaml

# 15. Meta reklam planı
python scripts/generate_meta_ads_plan.py \
  --agent meta_ads_manager \
  --context business_context.yaml

# 16. YouTube stratejisi (otorite için)
python scripts/generate_youtube_strategy.py \
  --agent youtube_strategy_agent \
  --context business_context.yaml

# 17. İş puan kartı — her ay
python scripts/generate_business_scorecard.py \
  --agent business_scorecard_agent \
  --context business_context.yaml
```

---

## Dashboard Kullanımı

```bash
# Dashboard'u başlat
python dashboard/server.py

# Tarayıcıda aç
# http://localhost:8765
```

Dashboard şunları gösterir:
- Tüm agent'ların durumu
- Her agent'ın bellek dosyaları
- Son üretilen çıktılar

API anahtarı gerekmez. Sadece yerel çalışır.

---

## Kalite ve Test Komutları

```bash
# Tüm testleri çalıştır
python -m pytest

# Tüm checklists'i çalıştır
python scripts/run_checklist.py --all

# Spesifik agent'ı doğrula
python scripts/run_checklist.py --agent offer_architect

# YAML geçerliliğini kontrol et
python scripts/validate_yaml.py

# Agent yapısını doğrula
python scripts/validate_agent_structure.py

# Context'i sıkıştır (büyük konuşmalardan sonra)
python scripts/compact_context.py --agent offer_architect
python scripts/compact_context.py --all

# Eval'ları çalıştır
python scripts/run_evals.py --all
```

---

## Sık Yapılan Hatalar

### 1. Araştırma sinyalini doğrulanmış gibi kullanmak

```
YANLIŞ: Reddit'teki bir yoruma dayanarak tüm stratejiyi değiştirmek
DOĞRU: Sinyal "candidate" ise, birden fazla kaynaktan doğrulanana kadar bekle
```

### 2. Avatar'ı geniş tutmak

```
YANLIŞ: "30-50 yaş çalışan kadınlar"
DOĞRU: "Ayşe, 38, İstanbul finans sektörü yöneticisi, 2 çocuk, kronik yorgunluk"
```

### 3. Öğrenme fazında kampanyaya dokunmak

```
YANLIŞ: Reklam 3 günde sonuç vermedi, değiştir
DOĞRU: ~50 dönüşüm toplanana kadar bekle. Dokunursan sıfırdan başlarsın.
```

### 4. Fiyatı değer yığınından önce söylemek

```
YANLIŞ: "Programım 15.000 TL..."
DOĞRU: Önce değer yığınını göster (22.000 TL algılanan değer),
       sonra "ancak bugün 15.000 TL"
```

### 5. Vaka çalışmasında vague kalmak

```
YANLIŞ: "Müşterim çok memnun kaldı"
DOĞRU: "91 günde 14.3 kilo, sabah 5:30'da uyanmaya başladı, 3 ay önceki son takımı artık giyiyor"
```

### 6. Mock veriyi gerçek pazar verisi saymak

Sistem mock araştırma sonuçlarına `is_mock: true` ekler ve `mock://` URL'si kullanır. Bunları gerçek veriymiş gibi yorumlama.

---

## Sonraki Adımlar

Sistemi canlı veriyle çalıştırmak istediğinde [README.md](README.md) dosyasındaki "How To Add Real Providers Later" bölümüne bak. Gerçek API'ları aynı interface'ler arkasına ekleyebilirsin:

- `TAVILY_API_KEY` → web araştırması
- `FIRECRAWL_API_KEY` → web sayfası çıkarma
- `REDDIT_CLIENT_ID` + `REDDIT_CLIENT_SECRET` → Reddit araştırması
- `YOUTUBE_API_KEY` → YouTube içerik analizi
- `FACEBOOK_AD_LIBRARY_TOKEN` → reklam kütüphanesi

Tüm bu değişkenler `.env.example` dosyasında belgelenmiştir.
