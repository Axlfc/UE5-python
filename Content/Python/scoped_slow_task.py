import unreal
import time
import random


def scoped_slow_task_example():
    items = unreal.EditorUtilityLibrary.get_selection_set()

    with unreal.ScopedSlowTask(len(items), 'Processing items') as task:
        task.make_dialog(True)

        processed_items = 0
        for item in items:
            if task.should_cancel():
                show_cancel_confirmation_dialog()
                break

            task.enter_progress_frame(1, 'Processing {} ({}/{})'.format(item.get_actor_label(),
                                                                        processed_items, len(items)))
            
            # simulate long processing of the item
            time.sleep(random.uniform(0.1, 0.3))
            processed_items += 1


def nested_scoped_slow_task_example():
    items = unreal.EditorUtilityLibrary.get_selection_set()

    with unreal.ScopedSlowTask(len(items), 'Processing items') as task:
        task.make_dialog(True)
        
        processed_items = 0
        for item in items:
            if task.should_cancel():
                show_cancel_confirmation_dialog()
                break

            task.enter_progress_frame(1, 'Processing {} ({}/{})'.format(item.get_actor_label(),
                                                                        processed_items, len(items)))

            # simulate long processing of the item
            time.sleep(random.uniform(0.1, 0.3))
            
            numbers_to_count = int(random.uniform(20, 50))
            with unreal.ScopedSlowTask(numbers_to_count, 'Counting') as sub_task:
                sub_task.make_dialog(True)
                for current_number in range(0, numbers_to_count):
                    if sub_task.should_cancel():
                        show_cancel_confirmation_dialog()
                        return

                    sub_task.enter_progress_frame(1, 'Counting {} of {}'.format(current_number, numbers_to_count))
                    
                    # counting takes time
                    time.sleep(random.uniform(0.05, 0.15))

            processed_items += 1


def show_cancel_confirmation_dialog():
    unreal.EditorDialog.show_message('Operation canceled',
                                     'Operation canceled by user', unreal.AppMsgType.OK, unreal.AppReturnType.OK)


def ask_for_cancel_confirmation():
    user_confirmation = unreal.EditorDialog.show_message('Are you sure?', 'Are you 100% positive you want to cancel?',
                                                         unreal.AppMsgType.YES_NO_YES_ALL, unreal.AppReturnType.NO)
    if user_confirmation == unreal.AppReturnType.YES:
        pass
    if user_confirmation == unreal.AppReturnType.YES_ALL:
        return
