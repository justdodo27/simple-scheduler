from random import shuffle
import streamlit as st
from datetime import datetime, timedelta

emoji = [
    '🤪', '😎', '🐒', '🐕', '🐔', '🦤', '🦅', '🦫', '🦁', '🦍'
]

check = '✔️'

def count_group(group, schedule):
    n = 0
    for day in schedule:
        if group in day: n+=1
    return n

st.write("""
# Subarashi Plan Dentystów 🦷
""")

groups = st.slider("Ilość grup", 3, 10, 7)

days = st.slider("Ilość dni", 1, 20, 14)

groups_per_day = st.slider("Maksymalna liczba grup na dzień", 1, groups//2, 4)

st.write("""
# Zaznaczanie dla kapryśnych >_<
""")

blacklist = []

start_date = datetime(2022, 3, 21)

labels = []

weekdays = ["Pon", "Wt", "śr", "Czw", "Pt", "Sb", "Nd"]

for i in range(days):
    while start_date.weekday() not in [2,3,4]:
        start_date = start_date + timedelta(days=1)
    label = f"{start_date.day:0>2}-{start_date.month:0>2}-{start_date.year} {weekdays[start_date.weekday()]}"
    labels.append(label)
    start_date = start_date + timedelta(days=1)

def print_days(opt):
    return f"{opt:0>2}.  {labels[opt-1]}"

for i in range(groups):
    st.write(f'### Grupa {i+1} {emoji[i]}')
    blacklist.append(st.multiselect(
        "Jakie dni nie pasują?",
        [j+1 for j in range(days)],
        [],
        key=i+1,
        format_func=print_days
    ))
    st.write(f"Wybrano: {blacklist[i]}" )
    if days - len(blacklist[i]) < ((days*groups_per_day) / groups):
        st.write(f"Za dużo dni marudo!!!")

valid = True

def count_bl_days():
    temp = [[i+1, 0] for i in range(days)]

    for i in range(groups):
        for day in blacklist[i]:
            temp[day-1][1] += 1
    return temp


def blacklist_sort(days, blacklist):
    bl_days = count_bl_days()
    bl_days = sorted(bl_days, key=lambda x: x[1], reverse=False)
    return bl_days


if valid:
    groups_sequence = [[i+1, 0 - len(blacklist[i])] for i in range(groups)]
    shuffle(groups_sequence)
    groups_sequence = sorted(groups_sequence, key=lambda x: x[1], reverse=False)
    schedule = [[] for _ in range(days)]

    days_sort = [i for i in range(days)]

    days_sort = blacklist_sort(days_sort, blacklist)
    for day in days_sort:
        j = 0
        day_schedule = []
        groups_sequence = sorted(groups_sequence, key=lambda x: x[1], reverse=False)
        while j < groups_per_day:
            group = groups_sequence.pop(0)
            if count_group(group[0], schedule) == ((days*groups_per_day) / groups):
                continue
            if day[0] not in blacklist[group[0]-1]:
                day_schedule.append(group[0])
                group[1] += 1
                j += 1
            groups_sequence.append(group)
        schedule[day[0]-1] = day_schedule
    for i, s in enumerate(schedule):
        st.write(f"#### {labels[i]} : {*s,}")

    for i in range(groups):
        count = count_group(i+1, schedule)
        st.write(f"# Grupa {i+1} {emoji[i]} : {count} dni")