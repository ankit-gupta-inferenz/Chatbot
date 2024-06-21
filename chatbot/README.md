# Molly - AI Personal Style Advisor

## Description
Molly is an AI-based personal style advisor that assists users in various fashion-related tasks. It can process inputs in text or image format and responds with textual advice or product recommendations from partnered stores. Using advanced natural language processing powered by LangChain and OpenAI API, along with image recognition capabilities via YOLOv8, Molly provides personalized recommendations tailored to the user's preferences and queries.

## Branch Structure

### Master Branch (`master`):
- **Do not push to master branch** unless discussed with RA or at least 2 active members of the team.
- The `master` branch contains stable and production-ready code.
- It serves as the main branch where the production code is stored and backed up.

### Development Branch (`dev`):
- The `dev` branch is where active development takes place.
- It serves as a staging area for features or fixes before they are merged into the `master` branch.

### Pre-Development Branch (`predev`):
- The `predev` branch acts as a playground for experiments and initial development.
- It is the default branch where developers pull from and push their changes before they are ready for broader integration.

### Personal Branches (`user_task`, etc.):
- Personal branches are created by individual developers for specific tasks or features.
- Each developer creates a branch named after the issue it is created for, following a naming convention will be best title which can show the issue in the shortest manner.
- Developers work independently on their personal branches, making changes and commits.
- When the issue is complete, developers create a pull request to merge their changes into the `predev` branch for review and integration.

## GitHub Standard Process Guideline
Refer to the document created by Akshit Trivedi for standard processes while using git within the institution. [GitHub Standards and Processes Documentation](https://inferenztechpvtltd-my.sharepoint.com/:w:/g/personal/akshit_trivedi_inferenz_ai/EQtMTS_2WUpGkhawnNRhOLwBrOHOQe3ekSTRgGfJi0Weig?OR=Teams-HL&CT=1715584526761&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiI0OS8yNDAzMzEwMTgxNyIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ%3D%3D)

## Usage
To use Molly, follow these steps:
*Kindly before cloning Branch, please be in touch with active Repository Contributors.*
1. Clone the repository:
   ```bash
   git clone https://github.com/inferenz-ai/Molly.git
   ```
2. Navigate to the project directory:
   ```bash
   cd ./molly
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the chatbot:
   ```bash
   python manage.py runserver
   ```
5. Start interacting with Molly by typing your queries or commands.

## Contributors
- Het Thakar
- Sushil Suthar
- Adarsh Mishra - Active
- Vikas Rathod
- Akshit Trivedi - Active
- Sanny Chauhan
- Maharshi Shukla - Active
- Mit Parekh - Active
- Khushi Shah - Active
- Shreya Tiwari - Active
- Aliraza Panjwani - Active

## Troubleshooting
If you encounter any issues while using this project, refer to the troubleshooting section to find solutions or share your problem and solution to help others.

1. **Error While Uploading Image:** 
   - Error:
      ```bash
     No such file or directory: 'static/imgs/uploads/email_timestamp.png'
   - Solution: Create a folder named ‘uploads' under the path 'molly/static/imgs/uploads’.

2. **Error regarding logs folder:** 
   - Error:
      ```bash
     FileNotFoundError: [Errno 2] No such file or directory: 'logs/api_calls.log'
   - Solution: Create a folder named ‘logs' under the path 'Molly/logs’.

3. **Error regarding change in ownership of a local GIT repository:** 
   - Error:
      ```bash
     fatal: detected dubious ownership in repository at 'D:/Molly'
   - Solution: Add command git config --global --add safe.directory D:/Molly and later clone the repository from Github again. Additionally,another solution could be to just clone the repository in a different folder.

4. **Adding an Empty Folder to the Repository:**
   - Follow these steps to add an empty folder to your Git repository:
     1. Navigate to the directory where you want to create the empty folder.
     2. Create the folder or go to the empty folder.
     3. Inside that folder, create a `.gitignore` file with the following content:
        ```
        # Ignore everything in this directory
        *
        # Except this file
        !.gitignore
        ```
     4. Add, Commit, and push the `.gitignore` file to the repository. Push the empty folder along with  the `.gitignore` file as a content to the repository. If the folder has atleast one file(i.e. .gitignore file) it will be pushed to git.
        ```bash
        git add .
        git commit -m "Add .gitignore file to the empty folder"
        git push
        ```
   - After these steps, the empty folder will be successfully added to your Git repository.
