from typing import List, Dict, Tuple, Set, Any

class DataStructure:
    def process_items(self, items: List[int]) -> List[int]:
        for item in items:
            print(item)
        return items

    def process_dict(self, data: Dict[str, int]) -> Dict[str, int]:
        for key, value in data.items():
            print(f"{key}: {value}")
        return data

    def process_tuple(self, data: Tuple[int, str]) -> Tuple[int, str]:
        print(f"Number: {data[0]}, String: {data[1]}")
        return data

    def process_set(self, data: Set[str]) -> Set[str]:
        for item in data:
            print(item)
        return data

    def print_data_structure(self) -> Tuple[List[int], Dict[str, int], Tuple[int, str], Set[str]]:
        numbers = [1, 2, 3, 4]
        sample_dict = {"apple": 1, "banana": 2}
        sample_tuple = (1, "apple")
        sample_set = {"apple", "banana", "cherry"}

        processed_items = self.process_items(numbers)
        processed_dict = self.process_dict(sample_dict)
        processed_tuple = self.process_tuple(sample_tuple)
        processed_set = self.process_set(sample_set)

        return processed_items, processed_dict, processed_tuple, processed_set