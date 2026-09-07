class RouteParser():
    def __init__(self):
        pass

    def _parse_pattern(self, pattern: str) -> list[list]:
        chunks = []
        i = 0
        while i < len(pattern):
            if pattern[i] == '{':
                j = i + 1
                while pattern[j] != '}':
                    j += 1
                inner_string = pattern[i+1 : j]
                options = inner_string.split(',')
                options.sort()
                chunks.append(options)
                i = j + 1
            else:
                chunks.append([pattern[i]])
                i += 1
        return chunks
    
    def expand_pattern(self, pattern: str) -> list[str]:
        chunks = self._parse_pattern(pattern)
        results = []

        def backtrack(chunk_index: int, current_path: list[str]):
            if chunk_index == len(chunks):
                results.append("".join(current_path))
                return

            for option in chunks[chunk_index]:
                backtrack(chunk_index+1, [*current_path, option])

        backtrack(0, [])
        return results