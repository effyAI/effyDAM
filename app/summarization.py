from transformers import BartTokenizer, BartForConditionalGeneration
import re

model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def clean_text(input_text):
    cleaned_text = re.sub(r'\s+', ' ', input_text)
    cleaned_text = re.sub(r"""[^a-zA-Z0-9\s.!,"']""", '', cleaned_text)
    return cleaned_text

def generate_summary(text):
    new_text = clean_text(text)
    if len(new_text) >= 500:
        input_prompt  = f"""
        You have been provided with text of a file. Summarize the text as if you are providing a description of whole text. 
        Summary: {new_text} 
        """
        inputs = tokenizer.encode(input_prompt, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    else:
        return new_text
    
input_text = """
The Hubble Space Telescope has spotted water vapor erupting from the icy surface of Jupiter's moon Europa. 
The discovery strengthens the possibility of finding life elsewhere in our solar system, scientists say.
Europa has long been considered one of the top places to search for signs of life. 
It has a huge global ocean beneath its frozen crust. This ocean is about 100 kilometers deep and contains twice as much water as all of Earth's oceans combined.
"""

input_text2 = """
India  – A 901, Sai Miracle, Plot No 16/17/19, Sector 35 -E, Kharghar, Navi Mumbai 410210  
USA     UAE      Kenya  
  
Date:  19th September  2023  
To,  
Jainil  Patel  
A-301 Flora Avenue,  
Green City Road, Pal,  
Sura t, India  
 
Dear Jainil , 
Congratulations! We are pleased to extend an offer for an internship position at effyBiz Inc. We 
were impressed by your qualifications and enthusiasm during the application process, and we 
believe that your skills and passion will be a valuable addition to our team.  
Position:  Trainee Engineer   
Location: Remote / Online  
Managers Name: Mr. Novneet Patnaik  
 
During your internship at effyBiz Inc, you will have the opportunity to gain hands -on experience 
in various aspects of product development.  As an intern, you will work closely with our team of 
professionals, contributing to effyAI project . This internship will provide you with valuable 
exposure to the AI/ML field  and allow you to develop essential skills and knowledge.  
Terms and Conditions:  
Duration: 19th September  2023 to 30th November  2023  
Compensation: The internship is paid , and you will receive a monthly stipend of Rs. 7500/ - 
Working Hours : Your work schedule will be 48 hours per week . 
  
India  – A 901, Sai Miracle, Plot No 16/17/19, Sector 35 -E, Kharghar, Navi Mumbai 410210  
USA     UAE      Kenya  
  
Confidentiality:  During your internship, you will have access to sensitive information. 
Therefore, you will be required to sign a confidentiality agreement to protect the company's 
proprietary information.  
 
Please review this internship offer carefully. If you accept our offer, please sign and return a 
copy of this letter by 30th September  2023.  
 
We are excited to have you join our team, and we look forward to working with you. If you have 
any questions or require further clarification, please do not hesitate to contact me at 
mahesh@effybiz.com . Your performance during the internship will be evaluated for permanent 
role in our organization.  
Our evaluation process will include factors such as:  
• Job Performance : We will assess your performance in completing assigned tasks, 
meeting deadlines, and maintaining a high level of quality in your work.  
• Initiative and Proactiveness:  We will evaluate your ability to take initiative, show 
resourcefulness, and actively contribute to the team.  
• Adaptability and Learning Ability:  We will consider your willingness to learn, adapt to 
new challenges, and acquire new skills during the internship.  
• Teamwork and Collaboration:  We will assess your ability to work effectively in a team 
environment, communicate well with colleagues, and contribute to a positive work 
culture.  
• Professionalism:  We will evaluate your punctuality, professionalism, and adherence to 
company policies and guidelines.  
 
Please note that the evaluation process is comprehensive and takes into account various 
aspects of your performance and potential fit within our organization. While the internship 
evaluation does not guarantee a permanent position, it serves as a critical factor in our 
decision -making process.  
  
India  – A 901, Sai Miracle, Plot No 16/17/19, Sector 35 -E, Kharghar, Navi Mumbai 410210  
USA     UAE      Kenya  
 Once again, congratulations on your internship offer, and we wish you a successful and 
enriching experience at effyBiz Inc.  
For effyBiz Inc  
 
Mahesh Nair  
Founder & CEO  
effyBiz Inc  
"""

text3 = f"""
Subject: Application for Admission to B.Tech in Computer Science - Ravi Patel

Dear [College Name] Admissions Committee,

I hope this email finds you well. My name is Ravi Patel, and I am writing to express my keen interest in applying for admission to the B.Tech program in Computer Science at [College Name].

I have recently completed my higher secondary education with a strong focus on mathematics and computer science. My academic achievements and passion for technology have motivated me to pursue a career in computer science, and after thorough research, I believe that [College Name] is the ideal institution to nurture my academic and professional growth.

I am impressed by [College Name]'s reputation for academic excellence, state-of-the-art facilities, and a faculty renowned for their expertise in the field of computer science. The prospect of being a part of such an esteemed institution excites me, and I am confident that the challenging curriculum and collaborative learning environment will provide me with the knowledge and skills necessary to excel in my chosen field.

I have attached my completed application form, academic transcripts, and letters of recommendation to this email. Additionally, I would be happy to provide any further documentation or information as required for the admission process.

I am particularly drawn to [College Name] because of its commitment to fostering innovation and research in computer science. I am eager to contribute to and benefit from the vibrant academic community at your esteemed institution.

Thank you for considering my application. I am looking forward to the opportunity to contribute to the rich tapestry of [College Name] and to learn from the diverse perspectives of its student body. I am available for an interview at your convenience.

Please feel free to contact me via email at [Your Email Address] or by phone at [Your Phone Number] if you require any additional information.

Thank you for your time and consideration. I look forward to the possibility of studying at [College Name].

Sincerely,

Ravi Patel
[Your Contact Information]
"""

text4 = f"""
In the year 2050, the world underwent a radical transformation due to groundbreaking technological advancements. Artificial Intelligence (AI) became an integral part of everyday life, revolutionizing industries and reshaping the way people interacted with their surroundings. The fusion of biology and technology led to the development of cybernetic enhancements, enhancing human capabilities beyond imagination.

Space exploration reached unprecedented heights as humans established colonies on Mars and started mining asteroids for precious resources. Renewable energy sources dominated the global landscape, mitigating the impacts of climate change. Nanotechnology revolutionized medicine, enabling the eradication of various diseases at the molecular level.

With the rise of smart cities, interconnected devices formed a global network, optimizing traffic flow, energy consumption, and public services. Augmented Reality (AR) and Virtual Reality (VR) became ubiquitous, transforming entertainment, education, and professional training. Autonomous vehicles became the norm, reducing traffic accidents and reshaping urban infrastructure.

However, this technological utopia came with ethical challenges. Privacy concerns reached a critical point as surveillance technologies became omnipresent. The debate over AI rights sparked global discussions, and governments grappled with the ethical implications of creating sentient beings. Cybersecurity became a constant battle against increasingly sophisticated threats. ''', 
     
"""

# print("Original Text:")
# print(input_text)
# print("\nSumm1:")
# print(generate_summary(input_text))
# print("\nSumm2:")
# print(generate_summary(input_text2))
# print(len(generate_summary(input_text2)))

# print("\nSumm3:")
# print(generate_summary(text3))
# print("\nSumm4:")
# print(generate_summary(text4))

# print(generate_summary("   apple"))
