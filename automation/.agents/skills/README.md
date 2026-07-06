## How to Use the Skill
1. Create a requirements.txt file with your user stories:
      User can log in with valid credentials
   User sees an error message with invalid credentials
   User can reset their password via email
   
2. Run the generator:
      bash /home/hiennhan/Desktop/skills/test-bdd/generate-bdd-synth.sh requirements.txt ./my-output
   
3. Install dependencies:
      cd my-output
   npm install
   npx playwright install
   
4. Run the tests:
      npm test
   
✅ Verification
I tested the generator with a sample requirements.txt, and it successfully produced all the above boilerplate files in the output directory.