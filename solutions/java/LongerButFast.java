import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class LongerButFast {

    private static final Pattern PATTERN = Pattern.compile("\\Q,\\E");
    private static final Comparator<int[]> COMPARATOR =
            Comparator.comparing((int[] i) -> Integer.valueOf(i[0])).thenComparing(i -> Integer.valueOf(i[1]));
    private static final int[] EMPTY = new int[2];

    public static void main(final String... args) {
        final int[] theirs = create(args[0]);
        if (theirs == null) {
            throw new IllegalArgumentException();
        }
        final int[] result = LongerButFast.winningDie(theirs);
        if (result == null) {
            System.out.println();
        } else {
            System.out.println(toString(result));
        }
    }

    private static int[] create(final String dice) {
        final String[] sides = PATTERN.split(dice);
        return Arrays.stream(sides)
                .mapToInt(s -> Integer.parseInt(s))
                .toArray();
    }

    public static String toString(final int[] die) {
        return IntStream.of(die)
                .mapToObj(String::valueOf)
                .collect(Collectors.joining(","));
    }

    private static int[] winningDie(final int[] enemy) {
        final int dim = enemy.length;
        final int total = IntStream.of(enemy).sum();
        final int[] win = new int[total + 1];
        for (int i = 1; i <= total; i++) {
            for (final int j : enemy) {
                win[i] += ((i > j) ? 1 : 0) - ((j > i) ? 1 : 0);
            }
        }
        final Subanswers subanswers = new Subanswers();
        for (int dieNum = 0; dieNum < dim; dieNum++) {
            final int curDieNum = dieNum;
            for (int subsum = dieNum + 1; subsum <= total; subsum++) {
                final int curSubSum = subsum;
                final int[] possibility = IntStream.range(1, curSubSum - curDieNum + 1)
                        .mapToObj(last -> new int[]{win[last] + subanswers.get(curDieNum, curSubSum - last)[0], last})
                        .max(COMPARATOR).orElseThrow(IllegalStateException::new);
                subanswers.set(curDieNum + 1, curSubSum, possibility);
            }
        }
        if (subanswers.get(dim, total)[0] > 0) {
            final int[] ans = new int[dim];
            int cur = total;
            for (int i = 0; i < dim; i++) {
                final int side = subanswers.get(dim - i, cur)[1];
                ans[i] = side;
                cur -= side;
            }
            return ans;
        } else {
            return null;
        }
    }

    private static final class Subanswers {

        private final Map<Integer, Map<Integer, int[]>> subanswers = new HashMap<>();

        public void set(final int dieNum, final int subsum, final int[] values) {
            final Integer die = Integer.valueOf(dieNum);
            subanswers.computeIfAbsent(die, num -> new HashMap<>());
            final Map<Integer, int[]> subsums = subanswers.get(die);
            subsums.put(subsum, values);
        }

        public int[] get(final int dieNum, final int subsum) {
            final Integer die = Integer.valueOf(dieNum);
            if (!subanswers.containsKey(die)) {
                return EMPTY;
            }
            final Map<Integer, int[]> subsums = subanswers.get(die);
            return subsums.getOrDefault(subsum, EMPTY);
        }
    }
}
