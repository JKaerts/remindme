# Remindme: a few scripts for dealing with reminders

This repository contains a few python scripts, written for dealing with
all sorts of reminders.

## A simple example

Suppose we have a file called `reminders.csv` with contents

```
t,2021-01-09,Order new contacts
t,2021-03-06,Ask John if he finished reading the borrowed book
b,1973-01-12,Mom
```

Each line in the csv-file follows the format`<type>,<date>,<text>`. The types
are explained in detail below, the dates are in the format yyyy-mm-dd and the
text depends on the type of reminder.

If we now run the command `python remindme.py reminders.csv` on the date
2021-01-11, the output will be as follows:

```
Hello, these are your reminders for today:
* Order new contacts
* Mom has a birthday in 1 day(s)
```

I have configured Python's csv-parser to ignore whitespace following commas
so you can organize your csv as follows for better readability:

```
t, 2021-01-09, Order new contacts
t, 2021-03-06, Ask John if he finished reading the borrowed book
b, 1973-01-12, Mom
```

## The different types of reminders

The following types are defined:
- Tasks: Defined by making `t` the first field of a row. A task will be shown in
  the output when its date has passed. It will keep appearing until its entry is
  removed from the csv-file.
- Birthdays: Defined by making `b` the first field of a row. The date in the row
  should be the actual date of birth of the person. Once the next occurrence of
  the birthday is one day or less into the future, it will appear in the output
  of the program. This can be configured.
- Anniversaries: Defined by making `a` the first field of a row. Completely
  similar to birthdays but with other kinds of output.

## Customizing the behaviour of birthdays and anniversaries

Birthdays and anniversaries appear one day in advance in the output. This is to
maximize my chances to send a text or email the day itself. However, for some people
I want more time to prepare myself. This way I'm reminded early enough to buy a card
or gift. Compare the following two possible rows in the csv-file:

```
b, yyyy-mm-dd, acquaintance
b, yyyy-mm-dd, close friend, 10
```

The entry for the acquaintance is standard. I will be notified the day before. But the
entry for the close friend has a fourth field containing the number ten. This means that
ten days before his birthday, the program will start notifying me of his birthday. This
method works for any type of reminder, even tasks. However, I rarely have a use for this
outside of birthdays and anniversaries.

## The layout of the csv-file

The script `remindme.py` can handle a little more than an ordinary csv-file. While any
decent csv-file will work, the parser will ignore any blank lines and any lines starting
with a hash sign (`#`). These are comments. This way, you can organize your reminders:

```
# Tasks
t, ...
t, ...

# Friends
b, ...
b, ...

# Family
b, ...
b, ...

# Anniversaries
a, ...
a, ...
```

With tasks, you can exploit the fact that csv-fields can span multiple lines to create
multiline-tasks:

```
t, yyyy-mm-dd, "A task
  whose explanation
  spans multiple
  lines"
```

Try to indent each subsequent line with two spaces for readability in both the csv-file
and the actual output.

## Other utilities

The script `jubileechecker.py` takes two arguments: a csv-file that can be processed
by `remindme.py` and a year. It will check the birthdays and anniversaries in the file
for any jubilees that will appear in the given year. I have defined a jubilee to occur
every five years. Running this script every year will alert you of birthdays and
anniversaries to pay special attention to in the coming year. This way you can edit
the notification window accordingly.
