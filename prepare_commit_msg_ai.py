
from openai import OpenAI
import subprocess as sp
client = OpenAI()

content_system = """
You are an assistant specialized in analyzing the quality of commits for GitHub, 
using the output of the git diff command and classifying them according to the following recommendations:

RECOMMENDATIONS (type - meaning):
initial commit - commits for when the diff file is empty. 
feat - Commits of type feat indicate that your code snippet is adding a new feature (related to MINOR in semantic versioning). 
fix - Commits of type fix indicate that your committed code snippet is solving a problem (bug fix), (related to PATCH in semantic versioning). 
docs - Commits of type docs indicate that there have been changes in the documentation, such as in your repository’s Readme. (Does not include code changes). 
test - Commits of type test are used when changes are made to tests, whether creating, altering, or deleting unit tests. (Does not include code changes). 
build - Commits of type build are used when modifications are made to build files and dependencies. 
perf - Commits of type perf are used to identify any code changes related to performance. 
style - Commits of type style indicate that there have been changes related to code formatting, semicolons, trailing spaces, lint… (Does not include code changes). 
refactor - Commits of type refactor refer to changes due to refactoring that do not alter functionality, such as a change in the way a part of the screen is processed but maintaining the same functionality, or performance improvements due to a code review. 
chore - Commits of type chore indicate updates to build tasks, admin configurations, packages… such as adding a package to gitignore. (Does not include code changes). 
ci - Commits of type ci indicate changes related to continuous integration. 
raw - Commits of type raw indicate changes related to configuration files, data, features, parameters. 
cleanup - Commits of type cleanup are used to remove commented code, unnecessary snippets, or any other form of source code cleanup, aiming to improve its readability and maintainability. 
remove - Commits of type remove indicate the deletion of obsolete or unused files, directories, or functionalities, reducing the project’s size and complexity and keeping it more organized.

OUTPUT:
type recommendation - description of changes in up to 6 words in portuguese
"""

content_user = sp.run(['git', 'diff', '--staged'], capture_output=True, text=True).stdout

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": content_system},
        {
            "role": "user",
            "content": content_user
        }
    ]
)

print(completion)

resposta = completion.choices[0].message.content
file = open('temp_msg', 'w')
file.write(resposta)
file.close()
