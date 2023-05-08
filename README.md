# Java Assignment Dataset Builder

The "Java Assignment Dataset Creator" is a tool that simplifies the process of generating a structured dataset from a folder containing over 1000 Java assignments. Its purpose is to extract relevant information from each assignment and organize it into a format that is easy to analyze and explore. The assignment files follow a specific naming convention:  `Assignment#[AssignmentNumber]_[StudentID]_attempt_[Date]-[Time]_Problem_[ProblemNumber]`.

## Organizing and creating the Dataset
To ensure a well-structured dataset, the tool transforms the file names into a standardized format: `Assignment[AssignmentNumber]_Problem[ProblemNumber]_[StudentID]`. This simplified naming convention makes it easier to retrieve and sort the data, facilitating efficient analysis and exploration. The extracted features and labels are combined to create a comprehensive DataFrame, which serves as the foundation of the dataset.

## Result
![The final dataset](https://user-images.githubusercontent.com/89030659/236932753-d89ad813-7fc7-4460-960f-0e80a7d0b165.png)

### WIP..
create a label and train a simple model to classify the data
