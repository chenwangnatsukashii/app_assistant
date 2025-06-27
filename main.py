import os
from PIL import Image
from utils import load_image, draw_box
from engine import LMMEngineGemini
from agents.grounding import GroundingAgent


# def load_vqa_data(json_path):
#     """Load VQA data from JSON file."""
#     with open(json_path, 'r', encoding='utf-8') as f:
#         data = []
#         for line in f:
#             item = json.loads(line)
#             data.append(item)  # Save complete data structure
#     return data


# def save_vqa_data(json_path, data):
#     """Save VQA data back to JSON file."""
#     with open(json_path, 'w', encoding='utf-8') as f:
#         for item in data:
#             json_line = json.dumps(item, ensure_ascii=False)
#             f.write(json_line + '\n')

# def handleVQA():
#     # Get file paths from user input
#     json_path = input("Enter the JSON file path: ")
#     image_dir = input("Enter the image directory path: ")
    
#     # Load VQA data
#     vqa_data = load_vqa_data(json_path)
#     print(f"Loaded {len(vqa_data)} items")
    
#     # Initialize model
#     engine = LMMEngineGemini(model="gemini-2.0-flash")
#     referring_agent = ReferringAgent(engine=engine)

#     # Process all data
#     for idx, item in enumerate(vqa_data, 1):
#         try:
#             image_path = f"{image_dir}/{item['image']}"
#             question = item['question']
            
#             print(f"\nProcessing item {idx}/{len(vqa_data)} ({idx/len(vqa_data)*100:.2f}%):")
#             print(f"Image: {item['image']}")
#             print(f"Question: {question}")
            
#             image_bytes = load_image(image_path)
#             if image_bytes:
#                 response = referring_agent.ReferringQuestionAnswer(
#                     image_bytes=image_bytes, 
#                     question=question
#                 )
#                 print(f"Answer: {response}")
                
#                 # Save answer to data
#                 item['answer'] = response
#             else:
#                 print(f"Failed to load image: {image_path}")
#                 item['answer'] = "Failed to load image"
                
#         except Exception as e:
#             print(f"Error processing data: {str(e)}")
#             item['answer'] = f"Processing error: {str(e)}"
#             continue
        
#         # Save progress every 10 items
#         if idx % 10 == 0:
#             print(f"\nSaving progress... {idx}/{len(vqa_data)}")
#             save_vqa_data(json_path, vqa_data)
    
#     # Final save
#     print("\nSaving all results...")
#     save_vqa_data(json_path, vqa_data)
#     print("Processing complete!")

def handleGrounding(grounding_agent:GroundingAgent):
    # add your image path here
    image_path = ""
    # 修改问题，使其更明确地指向目标位置
    image_question = "我想要点击龙韵礼盒广告中的立即购买按钮，它在哪里?"
    
    # Load and resize image while preserving aspect ratio
    target_size = (700, 1400)  # Target size for resizing
    image_bytes, orig_size, scale_factors = load_image(image_path,target_size)
    if image_bytes is None:
        print("load image failed")
        return
        
    # Get coordinates from model
    coordinates_str = grounding_agent.Grounding(image_bytes, image_question)
    
    try:
        # Convert string coordinates to list of integers
        coordinates = eval(coordinates_str)
        
        if len(coordinates) == 4:
            # Save the output image to desktop
            output_path = os.path.expanduser("~/Desktop/output.png")
        
            
            if draw_box(image_path, coordinates, output_path, scale_factors):
                
                # Calculate and print the scaled coordinates
                scaled_coords = [
                    int(coordinates[0] * scale_factors[0]),
                    int(coordinates[1] * scale_factors[1]),
                    int(coordinates[2] * scale_factors[0]),
                    int(coordinates[3] * scale_factors[1])
                ]
                print(f"缩放后的坐标: {scaled_coords}")
            else:
                print("绘制边框失败")
        else:
            print("获取的坐标格式不正确")
    except Exception as e:
        print(f"处理坐标时出错: {e}")
    


def main():
    engine = LMMEngineGemini(model="gemini-2.5-flash")
    grounding_agent = GroundingAgent(engine=engine)
    handleGrounding(grounding_agent=grounding_agent)

if __name__ == "__main__":
    main()

