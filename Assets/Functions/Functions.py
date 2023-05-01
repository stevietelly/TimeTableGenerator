from typing import List, Union
from Logic.DateTime.Time import Time
from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime
from Logic.Structure.Session import Session



def get_data_list(data_list: Union[List[Day], List[DayTime], List[Time]], num_units: int, start_point: Union[Day, Time, DayTime], direction: str) -> List:
    """
    Returns a list of data items from data_list starting from the start_point,
    in the specified direction and number of units, or until the end of the list
    if num_units is 0 (infinite).

    :param data_list: the list of data items to traverse
    :param num_units: the number of units to traverse, or 0 for infinite
    :param start_point: the item to start the traversal from
    :param direction: the direction to traverse in, either "before" or "after"
    :return: a list of data items
    """
    if start_point not in data_list:
        raise ValueError(f"Start point {start_point} not found in data list")

    start_index = data_list.index(start_point)
    if direction == "before":
        start_index -= 1
    elif direction != "after":
        raise ValueError(f"Invalid direction {direction}, must be 'before' or 'after'")

    result = []
    count = 0

    # Traverse the data list until the specified number of units have been reached,
    # or until the end of the list if num_units is 0.
    if direction == "after":
        for i in range(start_index+1, len(data_list)):
        
            result.append(data_list[i])
            count += 1
            if num_units != 0 and count >= num_units:
                break
    elif direction == "before" and num_units != 0:
       
        for i in range(start_index, len(data_list)):
            i += 1
            result.append(data_list[-i])
            count += 1
            if num_units != 0 and count >= num_units:
                break

    if num_units == 0:
        # Traverse to the end of the list if num_units is 0.
        if direction == "before":
            result = data_list[:start_index+1][::-1]
        else:
            result = data_list[start_index+1:]

    return result

def sort_sessions(sessions: List[Session]) -> List[Session]:
    """
    Sorts a list of sessions using the merge sort algorithm based on their DayTime attribute.

    Args:
        sessions (List[Session]): The list of sessions to sort.

    Returns:
        List[Session]: The sorted list of sessions.
    """
    # Base case: If the list has one or fewer items, it is already sorted
    if len(sessions) <= 1:
        return sessions

    # Recursive case: Split the list in half and recursively sort each half
    mid = len(sessions) // 2
    left_half = sessions[:mid]
    right_half = sessions[mid:]
    left_sorted = sort_sessions(left_half)
    right_sorted = sort_sessions(right_half)

    # Merge the sorted halves into a single sorted list
    sorted_sessions = []
    i, j = 0, 0
    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i].daytime <= right_sorted[j].daytime:
            sorted_sessions.append(left_sorted[i])
            i += 1
        else:
            sorted_sessions.append(right_sorted[j])
            j += 1
    sorted_sessions.extend(left_sorted[i:])
    sorted_sessions.extend(right_sorted[j:])
    return sorted_sessions

    
   