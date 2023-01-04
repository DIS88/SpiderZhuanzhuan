import time


def deco_with_param(param):
	def decorate(func):
		caches = {}
		counter = 0
		duration = 0

		def inner(*args, **kwargs):
			nonlocal counter, duration
			st = time.time()
			counter += 1
			# print(param)
			if args in caches:
				ret = caches[args]
			else:
				ret = func(*args, **kwargs)
				duration += time.time() - st
				caches[args] = ret
			print(f"Counter {counter} times, duration {round(duration)}s")
			return ret

		return inner

	return decorate


@deco_with_param("a")
def test(word):
	time.sleep(2)
	return word.upper()


print(test("word"))
print(test("word"))
print(test("word1"))
