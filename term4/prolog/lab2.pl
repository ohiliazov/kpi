:- initialization(main).

main :-
    fetch_numbers_from_file(Numbers),!,
    include(is_square_root_of_odd_number, Numbers, SquareRootsOfOddNumbers),
    write_output(SquareRootsOfOddNumbers).

fetch_numbers_from_file(Numbers) :-
    open('data.txt', read, FileWithNumbers),
    read_file(FileWithNumbers, Numbers),
    close(FileWithNumbers).

read_file(Stream, []) :-
    at_end_of_stream(Stream).

read_file(Stream,[X|L]) :-
    \+ at_end_of_stream(Stream),
    read(Stream, X),
    read_file(Stream, L).

write_output(SquareRootsOfOddNumbers) :-
    open('output.txt', write, FileWithCount),
    length(SquareRootsOfOddNumbers, Count),
    write(FileWithCount, 'Number of square roots of odd numbers: '),
    write(FileWithCount, Count),
    write(FileWithCount, '\nNumbers: '),
    write(FileWithCount, SquareRootsOfOddNumbers),
    write_ln(SquareRootsOfOddNumbers),
    close(FileWithCount).

is_square_root_of_odd_number(X) :-
    SquareRootOfX is integer(rationalize(sqrt(X))),
    X is SquareRootOfX^2,
    1 is SquareRootOfX mod 2.
