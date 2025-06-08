import json
from utils import load_image
from engine import LMMEngineGemini
from referringagent import ReferringAgent


def load_vqa_data(json_path):
    """Load VQA data from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = []
        for line in f:
            item = json.loads(line)
            data.append(item)  # Save complete data structure
    return data


def save_vqa_data(json_path, data):
    """Save VQA data back to JSON file."""
    with open(json_path, 'w', encoding='utf-8') as f:
        for item in data:
            json_line = json.dumps(item, ensure_ascii=False)
            f.write(json_line + '\n')


def main():
    # Get file paths from user input
    json_path = input("Enter the JSON file path: ")
    image_dir = input("Enter the image directory path: ")
    
    # Load VQA data
    vqa_data = load_vqa_data(json_path)
    print(f"Loaded {len(vqa_data)} items")
    
    # Initialize model
    engine = LMMEngineGemini(model="gemini-2.0-flash")
    referring_agent = ReferringAgent(engine=engine)

    # Process all data
    for idx, item in enumerate(vqa_data, 1):
        try:
            image_path = f"{image_dir}/{item['image']}"
            question = item['question']
            
            print(f"\nProcessing item {idx}/{len(vqa_data)} ({idx/len(vqa_data)*100:.2f}%):")
            print(f"Image: {item['image']}")
            print(f"Question: {question}")
            
            image_bytes = load_image(image_path)
            if image_bytes:
                response = referring_agent.ReferringQuestionAnswer(
                    image_bytes=image_bytes, 
                    question=question
                )
                print(f"Answer: {response}")
                
                # Save answer to data
                item['answer'] = response
            else:
                print(f"Failed to load image: {image_path}")
                item['answer'] = "Failed to load image"
                
        except Exception as e:
            print(f"Error processing data: {str(e)}")
            item['answer'] = f"Processing error: {str(e)}"
            continue
        
        # Save progress every 10 items
        if idx % 10 == 0:
            print(f"\nSaving progress... {idx}/{len(vqa_data)}")
            save_vqa_data(json_path, vqa_data)
    
    # Final save
    print("\nSaving all results...")
    save_vqa_data(json_path, vqa_data)
    print("Processing complete!")


if __name__ == "__main__":
    main()

