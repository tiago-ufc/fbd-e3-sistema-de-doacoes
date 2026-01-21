🤝 Contributing to Donation System
    
    First off, thank you for taking the time to contribute! This project thrives on collective effort. To keep the codebase clean and stable, we follow a specific workflow.

🌿 Our Workflow: Fork & Incremental Merges

    We use a Forking Workflow. This means you don't push directly to the main repository. Instead, you push to your own copy and request a review.

Set Up Your Fork
  1.Fork the main repository to your own GitHub account.
  2.Clone your fork locally:

    git clone https://github.com/tiago-ufc/fbd-e3-sistema-de-doacoes.git

  3.Connect to the original:
  This allows you to pull the latest changes from the group.
  
    git remote add upstream https://github.com/tiago-ufc/fbd-e3-sistema-de-doacoes.git

Working on Features:
  Always create a new branch for every task. Never work directly on main.

    git checkout -b feature/name-of-your-task

Keep Your Branch Updated
  Before submitting your work, make sure it’s compatible with the latest group code:

  Fetch the latest changes: 
  
    git fetch upstream

  Merge them into your feature branch: 
    
    git merge upstream/main

  Resolve any conflicts locally.

Submitting a Pull Request

  Push your branch to your fork: 
  
    git push origin feature/name-of-your-task

  Go to the original repository on GitHub and click "New Pull Request".
  We prefer small, frequent PRs rather than one massive update. This makes debugging much easier for everyone!

Coding Standards

  Keep them descriptive (e.g., feat: add date filter to campaign search instead of fix: updates).
  When modifying the database logic, always test your SQL queries locally before pushing.
  Use the existing Panel theme components to keep the look professional.
