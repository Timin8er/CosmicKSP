PARAMETER event_name, event_time.

UNTIL TIME:SECONDS >= event_time{

    LOCAL next_countdown_step TO event_time - FLOOR(event_time - TIME:SECONDS).

    WAIT UNTIL TIME:SECONDS >= next_countdown_step.

    LOCAL remaining_time TO CEILING(event_time - TIME:SECONDS).
    print(event_name + " in T-" + remaining_time + "s").
}