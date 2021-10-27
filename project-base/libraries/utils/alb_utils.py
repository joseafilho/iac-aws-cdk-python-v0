from aws_cdk import (
    aws_elasticloadbalancingv2 as alb
)

from aws_cdk.aws_elasticloadbalancingv2 import (
    IApplicationListener,    
    IApplicationLoadBalancerTarget
)

from aws_cdk.core import (
    Duration
)

class ALBUtils():

    @staticmethod
    def AddTargetInListener(id: str, alb_listener: IApplicationListener, target: IApplicationLoadBalancerTarget, port: int, priority: int, health_check_path: str, host_header: str, path: str = ''):
        rules = [alb.ListenerCondition.host_headers([host_header])]

        if path.strip() != '':
            rules.append(alb.ListenerCondition.path_patterns([path]))
        
        alb_listener.add_targets(
            id = id,
            target_group_name = id,
            port = port,
            protocol = alb.ApplicationProtocol.HTTP,
            targets = [target],
            conditions = rules,
            health_check = alb.HealthCheck(
                healthy_threshold_count = 5,
                path = health_check_path,
                timeout = Duration.seconds(2),
            ),
            priority = priority
        )