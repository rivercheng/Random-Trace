(defn generateRandomValue [dist params]
  let [value nil]
  (cond
    (= dist "lognormal") 
            (let [[sigma scale] params]
              (random.lognormal sigma scale))
    (= dist "genextreme")
            (let [[a b c] params]
              (random.genextreme a b c))
    (= dist "weibull")
            (let [[a loc scale] params]
              (random.weibull a loc scale))
    (= dist "constant")
            params))

(defn 
  "return the name of the related axis of an action"
  related_value [action]
  (let [axis (nth (lookupTable action) 0)]
    (str "(state " axis ")")))

(defn 
  related_axis [action]
  (nth (lookupTable action) 0))

(defn
  chooseAction [continueDict state]
  (let [action (state :prevAction)
        axis   (related_axis action)
        v      (eval (read-string (related_value action)))
        [p_continue p_reverse] (((continueDict axis) v) action)
        rand   (random.nextDouble)]
    (cond (<= rand p_continue) action
          (<= rand (+ p_continue p_reverse)) (reverseTable action))))

(defn rateMove [popularity_curr, popularity_plus, popularity_minus]
  (let [ratePlus (/ popularity_plus popularity_curr)
        rateMinus (/ popularity_minus popularity_curr)]
    [ratePlus rateMinus]))

(defn selectAxis [popularity]
  (let [highest filter #(== 0 (val %) popularity)]
    (if (empty? highest)
      (let [new_map (map #([(key %) (/ 1 (val %))]) popularity)
            res_map (reduce #([(key %1) (val %1)] 











       
