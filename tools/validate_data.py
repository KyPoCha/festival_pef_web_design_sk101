#!/usr/bin/env python3
"""Kontrola konzistence datové základny festivalu (data.json).

Použití:  python3 tools/validate_data.py [cesta/k/data.json]

Skript používá pouze standardní knihovnu Pythonu 3.9+. Je to vývojový nástroj
týmu, web samotný ho ke spuštění nepotřebuje. Při nalezení chyby končí
návratovým kódem 1.
"""
import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

MIN_DAYS, MIN_VENUES, MIN_PERFORMERS, MIN_EVENTS = 3, 2, 60, 60
WEEKDAYS = ["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"]

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def index(items, kind):
    """Vrátí slovník id -> položka a ohlásí duplicitní id a slugy."""
    by_id = {}
    slugs = Counter()
    for item in items:
        item_id = item.get("id")
        if not item_id:
            err(f"{kind}: položka bez id: {str(item)[:60]}")
            continue
        if item_id in by_id:
            err(f"{kind}: duplicitní id {item_id}")
        by_id[item_id] = item
        if "slug" in item:
            slugs[item["slug"]] += 1
    for slug, count in slugs.items():
        if count > 1:
            err(f"{kind}: duplicitní slug '{slug}' ({count}×)")
    return by_id


def require_text(item, fields, kind):
    for field in fields:
        value = item.get(field)
        if not isinstance(value, str) or not value.strip():
            err(f"{kind} {item.get('id')}: chybí nebo je prázdné pole '{field}'")


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "data.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    for key in ("festival", "days", "venues", "tracks", "eventTypes", "performerTypes",
                "levels", "languages", "countries", "performers", "events"):
        if key not in data:
            err(f"chybí hlavní klíč '{key}'")
    if errors:
        return report(path, data)

    festival = data["festival"]
    tz = ZoneInfo(data["meta"]["timezone"])
    days = index(data["days"], "den")
    venues = index(data["venues"], "scéna")
    tracks = index(data["tracks"], "téma")
    event_types = index(data["eventTypes"], "typ programu")
    performer_types = index(data["performerTypes"], "typ účinkujícího")
    levels = index(data["levels"], "úroveň")
    languages = index(data["languages"], "jazyk")
    performers = index(data["performers"], "účinkující")
    events = index(data["events"], "položka programu")

    # --- minimální rozsah ze zadání
    for label, count, minimum in (("dny", len(days), MIN_DAYS), ("scény", len(venues), MIN_VENUES),
                                  ("účinkující", len(performers), MIN_PERFORMERS),
                                  ("položky programu", len(events), MIN_EVENTS)):
        if count < minimum:
            err(f"minimální rozsah: {label} = {count}, požadováno alespoň {minimum}")

    # --- festival a dny
    require_text(festival, ("name", "fullName", "description", "character", "startDate", "endDate"), "festival")
    start_date = date.fromisoformat(festival["startDate"])
    end_date = date.fromisoformat(festival["endDate"])
    day_dates = sorted(date.fromisoformat(d["date"]) for d in days.values())
    expected = [start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1)]
    if day_dates != expected:
        err("dny festivalu neodpovídají rozsahu startDate–endDate")
    if festival.get("year") != start_date.year:
        err("festival.year neodpovídá roku v startDate")
    for d in days.values():
        require_text(d, ("date", "weekday", "label", "opens", "closes"), "den")
        real = WEEKDAYS[date.fromisoformat(d["date"]).weekday()]
        if d["weekday"] != real:
            err(f"den {d['id']}: {d['date']} je {real}, v datech je '{d['weekday']}'")

    # --- scény
    for v in venues.values():
        require_text(v, ("slug", "name", "kind", "zone", "description"), "scéna")
        if not isinstance(v.get("capacity"), int) or v["capacity"] <= 0:
            err(f"scéna {v['id']}: neplatná kapacita")

    # --- účinkující
    for p in performers.values():
        require_text(p, ("slug", "name", "tagline", "bio", "website"), "účinkující")
        if p.get("type") not in performer_types:
            err(f"účinkující {p['id']}: neznámý typ '{p.get('type')}'")
        if p.get("country") not in data["countries"]:
            err(f"účinkující {p['id']}: neznámá země '{p.get('country')}'")
        if not p.get("trackIds"):
            err(f"účinkující {p['id']}: žádné téma")
        for t in p.get("trackIds", []):
            if t not in tracks:
                err(f"účinkující {p['id']}: neznámé téma '{t}'")
    names = Counter(p["name"] for p in performers.values())
    for name, count in names.items():
        if count > 1:
            err(f"účinkující: duplicitní jméno '{name}'")

    # --- položky programu
    by_venue = defaultdict(list)
    by_performer = defaultdict(list)
    for e in events.values():
        eid = e["id"]
        require_text(e, ("slug", "title", "description", "start", "end"), "položka programu")
        for field, table in (("type", event_types), ("trackId", tracks), ("dayId", days),
                             ("venueId", venues), ("level", levels)):
            if e.get(field) not in table:
                err(f"položka {eid}: neznámá hodnota {field}='{e.get(field)}'")
        if e.get("language") is not None and e["language"] not in languages:
            err(f"položka {eid}: neznámý jazyk '{e['language']}'")
        if not e.get("performerIds"):
            err(f"položka {eid}: žádný účinkující")
        if len(set(e.get("performerIds", []))) != len(e.get("performerIds", [])):
            err(f"položka {eid}: účinkující je uveden vícekrát")
        for pid in e.get("performerIds", []):
            if pid not in performers:
                err(f"položka {eid}: neznámý účinkující '{pid}'")
        try:
            start = datetime.fromisoformat(e["start"])
            end = datetime.fromisoformat(e["end"])
        except (KeyError, ValueError):
            err(f"položka {eid}: neplatný formát času")
            continue
        if start.tzinfo is None or end.tzinfo is None:
            err(f"položka {eid}: čas bez časového pásma")
            continue
        if start >= end:
            err(f"položka {eid}: začátek není před koncem")
        if (end - start) != timedelta(minutes=e.get("durationMinutes", -1)):
            err(f"položka {eid}: durationMinutes neodpovídá rozdílu start–end")
        local = start.replace(tzinfo=None).replace(tzinfo=tz)
        if local.utcoffset() != start.utcoffset():
            err(f"položka {eid}: posun {start.utcoffset()} neodpovídá pásmu {tz.key}")
        day = days.get(e.get("dayId"))
        venue = venues.get(e.get("venueId"))
        if day:
            if start.date().isoformat() != day["date"] or end.date().isoformat() != day["date"]:
                err(f"položka {eid}: datum neodpovídá dni {day['id']}")
            if start.time() < time.fromisoformat(day["opens"]) or end.time() > time.fromisoformat(day["closes"]):
                err(f"položka {eid}: mimo provozní dobu dne {day['id']} ({day['opens']}–{day['closes']})")
        if venue:
            cap = e.get("capacity")
            if cap is not None and (not isinstance(cap, int) or cap <= 0 or cap > venue["capacity"]):
                err(f"položka {eid}: kapacita {cap} neodpovídá scéně {venue['name']} ({venue['capacity']})")
            if e.get("registrationRequired") and cap is None:
                err(f"položka {eid}: rezervace je povinná, ale chybí kapacita")
            if not venue.get("indoor") and end.time() > time(22, 0):
                err(f"položka {eid}: venkovní scéna {venue['name']} končí po 22:00")
        by_venue[e.get("venueId")].append((start, end, eid))
        for pid in e.get("performerIds", []):
            by_performer[pid].append((start, end, eid))

    # --- kolize ve scéně a u účinkujících
    for label, table, names_by_id in (("scéna", by_venue, venues), ("účinkující", by_performer, performers)):
        for key, slots in table.items():
            slots.sort()
            for (s1, e1, id1), (s2, e2, id2) in zip(slots, slots[1:]):
                if s2 < e1:
                    name = names_by_id.get(key, {}).get("name", key)
                    err(f"kolize – {label} {name}: {id1} a {id2} se překrývají")

    # --- každá entita je v programu použita
    for pid, p in performers.items():
        if pid not in by_performer:
            err(f"účinkující {pid} ({p['name']}) nemá žádnou položku programu")
    for vid, v in venues.items():
        if vid not in by_venue:
            err(f"scéna {vid} ({v['name']}) nemá žádnou položku programu")
    used_days = {e.get("dayId") for e in events.values()}
    for did in days:
        if did not in used_days:
            err(f"den {did} nemá žádnou položku programu")
    used_tracks = {e.get("trackId") for e in events.values()}
    for tid, t in tracks.items():
        if tid not in used_tracks:
            warn(f"téma {tid} ({t['name']}) není v programu použito")

    # --- vstupenky
    for ticket in data.get("practical", {}).get("tickets", []):
        for did in ticket.get("validDayIds", []):
            if did not in days:
                err(f"vstupenka {ticket.get('id')}: neznámý den '{did}'")

    # --- krátké přestávky mezi vystoupeními téhož účinkujícího na různých scénách
    for pid, slots in by_performer.items():
        for (s1, e1, id1), (s2, e2, id2) in zip(slots, slots[1:]):
            if timedelta(0) <= (s2 - e1) < timedelta(minutes=15) and events[id1]["venueId"] != events[id2]["venueId"]:
                warn(f"{performers[pid]['name']}: jen {(s2 - e1).seconds // 60} min na přesun mezi {id1} a {id2}")

    return report(path, data)


def report(path, data):
    print(f"Soubor: {path}")
    if "events" in data and "performers" in data:
        events = data["events"]
        print(f"  dny: {len(data['days'])}   scény: {len(data['venues'])}   témata: {len(data['tracks'])}   "
              f"účinkující: {len(data['performers'])}   položky programu: {len(events)}")
        per_day = Counter(e.get("dayId") for e in events)
        per_venue = Counter(e.get("venueId") for e in events)
        per_type = Counter(e.get("type") for e in events)
        venue_names = {v["id"]: v["name"] for v in data["venues"]}
        print("  podle dne:   " + ", ".join(f"{k}: {v}" for k, v in sorted(per_day.items())))
        print("  podle scény: " + ", ".join(f"{venue_names.get(k, k)}: {v}" for k, v in sorted(per_venue.items())))
        print("  podle typu:  " + ", ".join(f"{k}: {v}" for k, v in per_type.most_common()))
    for w in warnings:
        print(f"UPOZORNĚNÍ: {w}")
    for e in errors:
        print(f"CHYBA: {e}")
    print(f"Výsledek: {len(errors)} chyb, {len(warnings)} upozornění")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
