import re
import os
import shutil


def copy(src, dst):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    shutil.copyfile(src, dst)


def replacer(file_name, source, destenition):
    with open(file_name, 'r+', encoding="utf8") as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(source, destenition)

    # Write the file out again
    with open(file_name, 'w', encoding="utf8") as file:
        file.write(filedata)


STATIC_PRE = ('assets',)
STATICLY_TAGS = ('src', 'href',)
WORKING_DIRECTORY = './'
BACKUP_DIRECTORY = './test'
staticly_pattern_template = '('

if len(STATICLY_TAGS) > 1:
    staticly_pattern_template += "|".join(STATICLY_TAGS) + ')'
    STATICLY_TAGS = staticly_pattern_template
else:
    STATICLY_TAGS = STATICLY_TAGS[0]

if len(STATIC_PRE) > 1:
    STATIC_PRE = '(' + "|".join(STATIC_PRE) + ')'
else:
    STATIC_PRE = STATIC_PRE[0]

regex_pattern = rf'''(src|href)=('|"{STATIC_PRE}.*?('|"))'''
static_pattern = re.compile(regex_pattern)

# همه فایل‌های HTML را پیدا کن
all_html_files_in_directory = [x for x in os.listdir(WORKING_DIRECTORY) if
                               x.split('.')[-1] in ['html', 'htm']]

# گرفتن بکاپ از فایل‌ها
for template in all_html_files_in_directory:
    copy(os.path.join(WORKING_DIRECTORY, template), BACKUP_DIRECTORY)

# پردازش فایل‌های HTML
for template in all_html_files_in_directory:
    file_path = os.path.join(WORKING_DIRECTORY, template)

    with open(file_path, 'r+', encoding="utf8") as file:
        lines = file.readlines()

    # بررسی وجود `{% load static %}`
    if not any("{% load static %}" in line for line in lines):
        lines.insert(0, "{% load static %}\n")  # افزودن در ابتدای فایل

    matches = []
    for line in lines:
        matches.append(re.findall(regex_pattern, line))

    matches = [x[0][1].replace('"', '') for x in matches if len(x) == 1]
    matches = set(matches)

    for i in matches:
        lines = [line.replace(i, "{% static '" + i + "' %}") for line in lines]

    # نوشتن تغییرات در فایل
    with open(file_path, 'w', encoding="utf8") as file:
        file.writelines(lines)
