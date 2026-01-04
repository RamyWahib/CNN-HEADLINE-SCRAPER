% Matrices, Vectors

clc, clearvars
load("data.mat")

numbers = [Politics, Technology, World, Sports];
biggest = 0;
for i = 1:length(numbers)
    if numbers(i) > biggest
        biggest = numbers(i);
    end
end
figure;
bar(numbers, 0.6, "green")
xlabel('Category'); 
ylabel('# of Headlines'); 
title('CNN NEWS HEADLINES');
labels = ["Politics" "Technology" "World", "Sports"];

x = 1:numel(numbers);    % x‑positions of bars

for i = 1:numel(numbers)
    text(x(i), numbers(i), labels(i), ...
        'HorizontalAlignment','center', ...
        'VerticalAlignment','bottom')
end


for i = 1:10
    disp(headlines(i, :))
end

